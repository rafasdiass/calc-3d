---
adr: 0005
title: PostgreSQL 16 + Alembic + JSONB para persistencia
status: accepted
date: 2026-05-31
deciders: [Atena, Ayla]
consulted: [Apolo, Hefesto]
informed: [Iris, Artemis, Hera]
---

# ADR-0005 — PostgreSQL 16 + Alembic + JSONB

## Contexto

A persistencia do calc-3d cloud precisa atender quatro requisitos simultaneos: (1) integridade referencial forte entre projeto, elementos, materiais, resultados, usuarios e tenant; (2) flexibilidade para guardar payloads variaveis — entrada de calculo, configuracoes de norma por projeto, resultados intermediarios cuja estrutura evolui rapido; (3) transacoes ACID porque salvar um projeto envolve escrever em multiplas tabelas atomicamente; (4) suporte a Row Level Security para multi-tenancy (ADR-0004).

A escolha do SGBD influencia tudo o resto: ORM, migrations, modelo de dominio, estrategia de backup, replicacao, custo operacional. SQLite (estado atual) nao escala para SaaS multi-tenant. As opcoes serias sao PostgreSQL 16, MongoDB e MySQL 8.

Migrations versionadas tambem precisam de decisao: mudar schema em producao sem perder dados nem integridade. Alembic e o padrao do mundo SQLAlchemy.

## Opcoes consideradas

1. **PostgreSQL 16 + Alembic + JSONB** — Pros: ACID completo; RLS nativo (suporta ADR-0004); JSONB com indices GIN para campos flexiveis (entrada de calculo, config de norma); integridade referencial via FK; CTEs e window functions para relatorios; replicacao logica madura; ecossistema (pgAdmin, pg_dump, pg_basebackup); SQLAlchemy 2.0 + asyncpg first-class. Cons: schema rigido para tabelas (overhead em prototipagem inicial); operacao um pouco mais cara que MySQL em managed services.
2. **MongoDB** — Pros: schema-less, prototipagem rapida; payloads complexos triviais. Cons: sem ACID multi-documento confiavel ate versao recente (e ainda com pegadinhas); sem RLS — multi-tenancy vira filtro na aplicacao sem defesa em profundidade; sem JOINs (lookups custosos); integridade referencial vira disciplina, nao garantia; replicacao do plano comercial cara; modelo errado para dominio relacional (projeto -> elementos -> resultados).
3. **MySQL 8** — Pros: simples, barato em managed services, JSON nativo. Cons: RLS nao existe (pode-se simular com VIEWs mas e fragil); JSON menos potente que JSONB (sem indice GIN equivalente); CTEs e window functions chegaram tarde e tem casos esquisitos; menos features para read replicas em logical replication; ecossistema de extensoes mais pobre que Postgres.

## Decisao

Adotamos **PostgreSQL 16** como SGBD unico, **Alembic** para migrations versionadas e **JSONB** para campos de payload flexivel onde modelagem rigida em colunas seria prematura ou ruidosa.

**Onde usar JSONB (sim)**:
- `projects.input_payload` — JSON de entrada do wizard leigo (geometria simplificada, opcoes inferidas).
- `projects.standards_config` — configuracao de quais versoes de norma aplicar (ver core/standards/registry).
- `calculations.intermediate_results` — resultados intermediarios cuja estrutura ainda evolui.
- `audit_log.payload` — diff e contexto de auditoria.

**Onde NAO usar JSONB**:
- Entidades de dominio principais (project, element, material, support, load, soil_layer) — colunas tipadas.
- Relacionamentos — FK reais, nao apontadores em JSON.
- Campos pesquisados/filtrados frequentemente — coluna indexada.

**Migrations com Alembic — politica de rollback**:
1. Toda migration tem `upgrade()` e `downgrade()` implementados. Migration sem downgrade e rejeitada em code review.
2. CI roda obrigatoriamente: `alembic upgrade head` em base limpa, depois `alembic downgrade -1` e novamente `upgrade head`. Quebra = barra de PR.
3. Migrations destrutivas (drop column, drop table) sao multi-step: release N adiciona coluna nova e copia, release N+1 para de escrever na antiga, release N+2 faz drop. Nunca dropar no mesmo deploy que adiciona substituto.
4. Em producao: snapshot logico (`pg_dump`) imediatamente antes da migration; rollback de plano A = `alembic downgrade`, plano B = restore do snapshot.
5. Migrations rodam com role dedicado que possui `BYPASSRLS` (ADR-0004), separado da role da aplicacao.
6. Alembic `env.py` configurado para detectar drift via `compare_type=True` e `compare_server_default=True`.

## Consequencias

- **Positivas**: ACID + RLS + JSONB cobre todos os requisitos de persistencia do MVP e alem; ecossistema maduro; alinhado com ADR-0001 (SQLAlchemy/asyncpg) e ADR-0004 (RLS); flexibilidade JSONB sem perder integridade; auditoria robusta; rollback testado em CI.
- **Negativas**: managed Postgres e ~20-30% mais caro que MySQL em alguns provedores; schema rigido exige decisao mais cuidadosa nas tabelas principais (vista positivamente como saudavel).
- **Riscos**: 
  - Abuso de JSONB virando bag-of-properties (mitigado: code review com checklist; campos JSONB precisam justificativa).
  - Migration destrutiva acidental em producao (mitigado: snapshot pre-migration + politica multi-step + role separado).
  - Migration que nao roda downgrade limpamente (mitigado: CI obriga round-trip up/down/up).
  - Indices GIN em JSONB pesados (mitigado: indexar so o que de fato e queryable).

## Referencias

- /Users/rafaeldias/IdeaProjects/calc-3d/docs/planning/03-DESIGN.md (Stack proposta — DB; Decisoes arquiteturais ADR-005)
- /Users/rafaeldias/IdeaProjects/calc-3d/docs/adr/0001-stack-backend-python-fastapi.md (SQLAlchemy 2.0 + asyncpg)
- /Users/rafaeldias/IdeaProjects/calc-3d/docs/adr/0004-multi-tenancy-tenant-id-rls.md (RLS depende de Postgres)
- Alembic docs: autogenerate, env.py, branching
- PostgreSQL 16 docs: JSONB, GIN indexes, Row Security
