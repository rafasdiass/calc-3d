---
adr: 0004
title: Multi-tenancy via tenant_id + Postgres Row Level Security
status: accepted
date: 2026-05-31
deciders: [Atena, Ayla]
consulted: [Apolo, Hefesto]
informed: [Iris, Artemis, Hera]
---

# ADR-0004 — Multi-tenancy via tenant_id + Postgres RLS

## Contexto

O calc-3d cloud serve multiplos clientes (escritorios de calculo, calculistas PJ, construtoras) e cada cliente tem seus projetos, elementos, materiais, relatorios. Vazamento cross-tenant e incidente P0 — projetos estruturais sao confidenciais e contem informacao comercial sensivel. A escolha do modelo de isolamento define seguranca, custo operacional e velocidade de desenvolvimento.

Existem tres estrategias classicas: (a) `tenant_id` como coluna em toda tabela com filtragem na aplicacao, (b) schema-per-tenant com schema dedicado por cliente, (c) database-per-tenant com instancia logica isolada. Cada uma tem perfil distinto de seguranca, custo de operacao, complexidade de migration e impacto em performance.

O design ja indica preferencia por `tenant_id` + RLS. Esta ADR consolida a decisao, documenta o mecanismo de injecao do tenant na sessao SQLAlchemy/asyncpg e registra a armadilha conhecida do pool de conexoes — vetor recorrente de vazamento em RLS quando mal implementado.

## Opcoes consideradas

1. **tenant_id em toda tabela + Postgres RLS** — Pros: 1 banco, 1 schema, custo operacional minimo; RLS e enforcement no SGBD (defesa em profundidade — se a aplicacao esquecer o filtro, o banco bloqueia); migrations triviais (rodam uma vez para todos os tenants); JOINs simples; backup e replicacao unicos. Cons: erro de configuracao do `app.tenant_id` na sessao = falso negativo silencioso (todos os tenants vazam); precisa disciplina de teste; queries cross-tenant administrativas exigem role com `BYPASSRLS`; armadilha do pool de conexoes (ver mecanismo abaixo).
2. **Schema-per-tenant** — Pros: isolamento mais visual; migrations podem ser rolled out gradualmente; backup por tenant trivial. Cons: explosao de schemas (1000 tenants = 1000 schemas), custo de migration N-vezes maior, complexidade de roteamento na aplicacao (search_path por request), JOINs cross-tenant impossiveis para analytics, ferramentas de monitoring lutam com tantos schemas.
3. **Database-per-tenant** — Pros: isolamento maximo, conformidade facil para clientes enterprise paranoicos, blast radius zero. Cons: custo operacional alto (provisionar, monitorar, fazer backup de N bancos), inviavel para tier basico/free, deploy de migration vira projeto, conexao por tenant explode pool de conexoes.

## Decisao

Adotamos **tenant_id como coluna em toda tabela de dominio + Postgres Row Level Security ativado por tabela**, com a politica padrao:

```sql
CREATE POLICY tenant_isolation ON <tabela>
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE <tabela> ENABLE ROW LEVEL SECURITY;
ALTER TABLE <tabela> FORCE ROW LEVEL SECURITY;
```

Mecanismo de injecao do `tenant_id` na sessao SQLAlchemy 2.0 + asyncpg:

1. Middleware FastAPI extrai `tenant_id` do JWT validado e armaza em ContextVar.
2. Event listener SQLAlchemy `before_cursor_execute` (ou `after_begin` na sessao async) executa `SET LOCAL app.tenant_id = :tid` no inicio de cada transacao. `SET LOCAL` garante escopo da transacao — ao commit/rollback, a setting evapora.
3. Event listener `reset` no checkin do pool (`PoolEvents.reset` ou `connect`/`checkout` do asyncpg) executa `RESET app.tenant_id` ou `DISCARD ALL` para garantir que a conexao volte ao pool sem residuo.
4. Role da aplicacao **sem** `BYPASSRLS`. Migrations rodam com role separado que possui `BYPASSRLS`.
5. Cross-tenant analytics em jobs offline com role dedicado, auditado.

**Armadilha conhecida do pool**: sem `RESET` no checkin, a conexao pode voltar para o pool com `app.tenant_id` antigo definido em escopo de sessao (nao `LOCAL`). Se a proxima request esquecer o `SET`, ela herda o tenant errado e o RLS deixa passar. Mitigacoes obrigatorias:

- Usar **sempre** `SET LOCAL` (escopo transacao), nunca `SET` puro.
- Adicionar `RESET app.tenant_id` no hook de checkin do pool como cinto-e-suspensorio.
- Teste de integracao que pega conexao A com tenant X, devolve, pega B com tenant Y, e valida que B nao enxerga linhas de X.
- Auditoria: query sem `app.tenant_id` setado deve falhar com erro explicito (politica RLS sem default permissivo).

## Consequencias

- **Positivas**: 1 banco / 1 schema / custo operacional baixo; defesa em profundidade (app + RLS); migrations simples; analytics cross-tenant via role administrativo; suporta milhares de tenants sem mudanca de arquitetura.
- **Negativas**: complexidade adicional na configuracao do pool; teste de regressao obrigatorio para o mecanismo de injecao; queries administrativas exigem role separado com `BYPASSRLS`.
- **Riscos**: 
  - Esquecer `SET LOCAL` = vazamento (mitigado: hook centralizado obrigatorio + teste de integracao).
  - `RESET` no checkin nao executado por bug do driver = vazamento (mitigado: usar `SET LOCAL` faz a setting morrer no commit, mesmo sem reset).
  - Migration acidental rodando sem `BYPASSRLS` falha (mitigado: role de migration explicitamente configurado no Alembic env.py).
  - Auditoria recomendada: log estruturado de toda query com `tenant_id` e alarme P0 em qualquer warning de "no current_setting('app.tenant_id')".

## Referencias

- /Users/rafaeldias/IdeaProjects/calc-3d/docs/planning/03-DESIGN.md (Multi-tenancy)
- PostgreSQL 16 docs: Row Security Policies
- SQLAlchemy 2.0 docs: PoolEvents, ConnectionEvents (`before_cursor_execute`, `reset`)
- asyncpg docs: connection setup hooks
