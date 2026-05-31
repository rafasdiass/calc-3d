---
documento: sprints com tasks atribuídas
versao: 1.0
data: 2026-05-31
sprint_length: 2 semanas
inicio_proposto: 2026-06-02 (segunda)
---

# 08 — SPRINTS E TASKS

## Convenções

- **Sprint** = 2 semanas
- **Task ID**: `S{n}-T{m}` (ex: `S0-T01`)
- **Owner**: Apolo (BE) · Íris (FE) · Hefesto (QA) · Artemis (TL/review) · Atena (arquitetura) · Hera (orquestração) · Hermes (varredura) · Gaia (docs) · Afrodite (clínico — fora deste projeto) · Ayla (PO/validação)
- **Estimativa**: pequeno (≤4h) · médio (1d) · grande (2-3d) · épico (semana)
- **DoD** = definition of done
- **Status**: ⏳ pendente · 🚧 em curso · ✅ feito · ⛔ bloqueado

---

## SPRINT 0 — Limpeza e fundação (semanas 1-2)

**Objetivo**: matar o legado morto, plantar o esqueleto. Nada de cálculo novo.

**Marco gate**: `curl localhost:8000/health` → 200 + signup/login + CI verde.

### Tasks

| ID | Task | Owner | Estim. | DoD |
|---|---|---|---|---|
| S0-T01 | Deletar arquivos descartáveis: `cmaker`, `interfaces/foundation_calculator_interface.py`, `interfaces/visualizador_ifc.py`, `main.py`, todos os `.DS_Store` | Apolo | pequeno | git diff confirma remoção, build não-existente (ok) |
| S0-T02 | Adicionar `.DS_Store`, `__pycache__/`, `.idea/`, `venv/`, `.env*` ao `.gitignore` | Apolo | pequeno | `git status` limpo após `find . -name .DS_Store` |
| S0-T03 | Reescrever `README.md` (escopo backend SaaS, sem PySide2/PyQt6) | Gaia | pequeno | review Ayla |
| S0-T04 | Criar `pyproject.toml` (Python 3.12, FastAPI, SQLAlchemy 2, Alembic, Pydantic 2, Celery, Redis, ruff, mypy, pytest) | Apolo | médio | `pip install -e .` funciona |
| S0-T05 | Criar layout de pastas `apps/api`, `core/`, `infra/`, `tests/` (vazias) | Apolo | pequeno | árvore conforme `03-DESIGN.md` |
| S0-T06 | Setup Docker + docker-compose dev (api + postgres + redis) | Apolo | médio | `docker compose up` sobe tudo |
| S0-T07 | FastAPI hello world: `/health`, `/version` | Apolo | pequeno | endpoint responde 200 |
| S0-T08 | Setup Alembic + primeira migration vazia | Apolo | pequeno | `alembic upgrade head` ok |
| S0-T09 | Schema base: `tenants`, `users` + RBAC enum | Apolo | médio | migration roda, model carrega |
| S0-T10 | Auth: signup, login, JWT (FastAPI Users) | Apolo | grande | suite de testes cobrindo signup/login/refresh |
| S0-T11 | Middleware multi-tenant: extrai `tenant_id` do JWT, injeta em deps | Apolo | médio | teste de IDOR (user A não vê user B) |
| S0-T12 | CI GitHub Actions: ruff + mypy strict + pytest + cobertura | Apolo | médio | PR de teste passa |
| S0-T13 | Configurar Sentry + structlog + Prometheus client | Apolo | médio | erro forçado aparece no Sentry |
| S0-T14 | Mover `calculators/`, `models/`, `services/sqlite_service.py` pra branch arquivo `_legacy/` (ainda não importado) | Apolo | pequeno | árvore reflete `03-DESIGN.md` |
| S0-T15 | Documentar ADR-001 (FastAPI), ADR-002 (sem 3D), ADR-005 (Postgres) | Atena + Gaia | médio | `docs/adr/*.md` |
| S0-T16 | Frontend: setup Vite + React + TS + shadcn/ui + TanStack Query, página landing + signup/login | Íris | grande | `pnpm dev` rende, login chama API e funciona |
| S0-T17 | E2E smoke: signup → login → criar projeto vazio (Playwright) | Hefesto | médio | CI roda smoke |
| S0-T18 | Code review do sprint inteiro | Artemis | médio | parecer técnico em `docs/reviews/sprint-0.md` |
| S0-T19 | War Room WR-002: motor FEM (proprio vs opstool/OpenSeesPy vs Pynite) — decisao registrada em docs/debates/WR-002-motor-fem.md, ADR-0003 atualizado de provisional pra accepted | Atena + Apolo + Hefesto | medio | ata + ADR atualizada |
| S0-T20 | Rate limiting (slowapi + Redis) por tenant: Free 60/min, Pro 600/min | Apolo | medio | testes de rate limit verdes |
| S0-T21 | Politica de backup Postgres: pg_basebackup diario, retencao 30d, runbook em docs/runbooks/backup.md | Apolo | pequeno | runbook revisado |
| S0-T22 | ZAP baseline scan no CI (job nao-bloqueante mas reportado) + janela de pen test externo agendada pra S6 | Hefesto | medio | CI roda zap, agenda pen test |
| S0-T23 | Cobertura pytest --cov-fail-under=80 POR MODULO (core/fem, core/design, core/geo, core/loads — nao agregada) | Hefesto | pequeno | CI falha se < 80% por modulo |
| S0-T24 | Prometheus SLIs desde dia 1: latencia p50/p95/p99 por endpoint, error rate, calc duration histogram + dashboard Grafana base + alerta Sentry SLO | Apolo | grande | dashboard rodando, alerta dispara em teste |
| S0-T25 | API versionada /api/v1/* + politica de deprecation documentada (ADR-0006) | Apolo | pequeno | OpenAPI mostra /v1 |
| S0-T26 | Audit_log REVOKE UPDATE/DELETE pra role app + teste adversarial RLS | Apolo | medio | testes verdes |
| S0-T27 | Mover laura-maio26.txt → docs/private/, atualizar .gitignore (.idea/, docs/private/, etc) | Apolo | pequeno | git status clean |
| S0-T28 | Mockup HTML estatico T-04 + T-10 (apenas HTML+Tailwind, sem React) — para Pausa 2 Rafael | Iris | grande | 2 paginas HTML servidas em /mockups/ |

**Riscos S0**:
- Aprender FastAPI Users (estimar +2 dias buffer)
- Setup CI macOS vs Linux (path issues)

---

## SPRINT 1 — Domínio + persistência (semanas 3-4)

**Objetivo**: modelar projeto, elementos estruturais, materiais. Persistir em Postgres com tipo. Sem cálculo ainda.

### Tasks

| ID | Task | Owner | Estim. | DoD |
|---|---|---|---|---|
| S1-T01 | Schema: `projects` (multi-tenant, RLS), `elements`, `materials` (catálogo), `load_cases`, `soil_profiles`, `soil_layers`, `calc_results`, `audit_log` | Apolo | grande | migration roda, ER diagrama em `docs/db/` |
| S1-T02 | Pydantic schemas IO: ProjectCreate/Read/Update, ElementCreate, etc. | Apolo | médio | OpenAPI rende |
| S1-T03 | Routers CRUD: `/projects`, `/projects/{id}/elements`, `/projects/{id}/soil-profile`, `/projects/{id}/loads` | Apolo | grande | testes de integração CRUD |
| S1-T04 | RLS Postgres: queries cross-tenant retornam zero | Apolo | médio | teste explícito |
| S1-T05 | Catálogo de materiais: concreto C20-C50, aço CA-25/50/60, perfis ISO + NBR (seed) | Apolo | médio | seed roda, query lista |
| S1-T06 | Biblioteca de tipos de solo brasileiros (12+ tipos com faixas de propriedades) | Apolo (consulta Atena) | médio | seed roda |
| S1-T07 | Tabela `standards` (NBR 6118:2014, NBR 6122:2022, etc) com `valid_from/to` | Apolo | pequeno | seed |
| S1-T08 | Frontend: Dashboard projetos (T-04), criar projeto vazio | Íris | grande | tela conforme T-04 |
| S1-T09 | Frontend: tela de configurações de conta (T-40 mínimo) | Íris | médio | |
| S1-T10 | Testes de integração CRUD completos | Hefesto | grande | cobertura > 70% no router |
| S1-T11 | Documentar OpenAPI exportado | Gaia | pequeno | `docs/api/openapi.yaml` no repo |
| S1-T12 | Code review | Artemis | médio | |
| S1-T13 | OpenAPI codegen TS: pacote @calc-engine/api-types gerado via openapi-typescript no CI; build falha se OpenAPI mudar sem regerar | Apolo + Artemis | medio | tipos consumidos pelo front |
| S1-T14 | Contract test BE↔FE com schemathesis: gera testes a partir do OpenAPI e roda no CI | Hefesto | medio | CI roda contract tests |
| S1-T15 | Feature flags: coluna JSONB `feature_flags` em `tenants` + helper `feature_enabled(tenant, flag)` | Apolo | pequeno | testes verdes |
| S1-T16 | i18n setup PT/EN com react-i18next, strings centralizadas em src/locales/, lingua default PT-BR | Iris | medio | toggle PT/EN funciona |

---

## SPRINT 2 — FEM nucleo (semanas 5-6)
**Objetivo**: nucleo do solver. Ainda sem dimensionamento.
Tasks: S2-T01 elemento barra 3D, S2-T02 assembler, S2-T03 solver scipy sparse, S2-T04 esforcos nas barras, S2-T05 apoios (fixo/rotulado/movel), S2-T06 cargas (nodal+distribuida).
Buffer 20%: 1.6 dias reservados.

## SPRINT 2b — FEM fixtures + endpoint (semanas 7-8)
**Objetivo**: 5 fixtures canonicas Sussekind validadas + endpoint operacional.
Tasks: S2b-T01 5 fixtures Sussekind, S2b-T02 endpoint POST /api/v1/projects/{id}/calculate sincrono, S2b-T03 testes E2E, S2b-T04 documentar OpenAPI, S2b-T05 review Artemis.

---

## SPRINT 3a — NBR 6118 vigas (semanas 9-10)
S3a-T01 registry NBR 6118 (cobrimento, gamma, fck/fctk), S3a-T02 flexao simples vigas (dominios 2/3, As, As'min/max, rho_min), S3a-T03 cisalhamento NBR 6118 modelo I, S3a-T04 ELS flecha, S3a-T05 ELS fissuracao wk, S3a-T06 5 fixtures Carvalho/Filho viga (nao TQS), S3a-T07 endpoint dimensionar viga.

## SPRINT 3b — NBR 6118 pilares + orquestrador (semanas 11-12)
S3b-T01 pilar compressao centrada, S3b-T02 pilar flexo-compressao 1a ordem, S3b-T03 pilar 2a ordem aprox, S3b-T04 deteccao dominio + sugestao, S3b-T05 orquestrador, S3b-T06 5 fixtures pilar Carvalho/Filho, S3b-T07 frontend tela T-30 com drill-down.

---

## SPRINT 4 — Geotecnia básica + sapata isolada NBR 6122 (semanas 9-10)

**Objetivo**: sapata isolada calculada de ponta-a-ponta com Terzaghi/Meyerhof + recalque elástico.

### Tasks

| ID | Task | Owner | Estim. | DoD |
|---|---|---|---|---|
| S4-T01 | `core/geo/soil_profile.py`: classe perfil multicamada com NA | Apolo | médio | testes |
| S4-T02 | `core/geo/bearing_capacity/terzaghi.py`: capacidade última + admissível | Apolo | grande | fixtures Velloso/Lopes |
| S4-T03 | Idem Meyerhof, Vesic, Brinch-Hansen | Apolo | grande | fixtures |
| S4-T04 | `core/geo/settlement/elastic.py` (Boussinesq) | Apolo | médio | fixtures |
| S4-T05 | `core/foundations/footing.py`: refatorar `sapata.py` atual pra usar geo + NBR 6122 | Apolo | grande | bate com cálculo manual |
| S4-T06 | Verificação NBR 6122: σ ≤ q_adm, recalque ≤ admissível, estabilidade tombo/escorregamento | Apolo | médio | |
| S4-T07 | Integração: sapata recebe esforços do FEM (N, Mx, My) | Apolo | médio | E2E |
| S4-T08 | Frontend: drill-down de sapata em T-30 | Íris | médio | |
| S4-T09 | Bench cruzado: 5 casos sapata vs Velloso/Lopes (NAO TQS — fora do escopo de validacao por decisao Ayla 2026-05-31) | Hefesto | medio | erro < 1% em todos os casos |
| S4-T10 | Review | Artemis | médio | |

---

## SPRINT 5a — Inferencia + cargas (semanas 15-16)
S5a-T01 cep_to_wind (NBR 6123 com base de dados de isopletas), S5a-T02 usage_to_live (NBR 6120), S5a-T03 geometry_inference (vao economico NBR 6118), S5a-T04 cargas vento (pressao dinamica + coef forma), S5a-T05 combinacoes NBR 8681 ELU/ELS, S5a-T06 testes.

## SPRINT 5b — Wizard + UX (semanas 17-18)
S5b-T01 endpoint /api/v1/projects/wizard, S5b-T02 wizard frontend 5 passos, S5b-T03 WS/SSE/polling pra T-15 progresso (decidido em ADR-0007), S5b-T04 UX teste com 3 usuarios reais ANTES da implementacao final, S5b-T05 E2E Playwright completo (5 passos + erros + PDF).

---

## SPRINT 6 — Relatório PDF + auditoria (semanas 13-14)

**Objetivo**: PDF profissional + log auditável. Fim da Fase 1, gate de release.

### Tasks

| ID | Task | Owner | Estim. | DoD |
|---|---|---|---|---|
| S6-T01 | `core/report/pdf_renderer.py` (refatora `report_generator.py` atual): capa, índice, memória passo-a-passo | Apolo | épico | PDF abre, citação inline em cada cálculo |
| S6-T02 | Gráficos 2D (matplotlib → PDF): planta de pilares, esquema viga, diagrama de momento | Apolo | grande | |
| S6-T03 | Lista de materiais (volume concreto, peso aço, área fôrma) | Apolo | médio | |
| S6-T04 | `audit_log` populado em cada cálculo (hash do input, versão motor, versão norma) | Apolo | médio | append-only confirmado |
| S6-T05 | Tela T-30 lista versões anteriores do projeto | Íris | médio | |
| S6-T06 | Endpoint `/projects/{id}/report.pdf` com cache | Apolo | médio | |
| S6-T07 | Pen test interno (Hefesto roda OWASP ZAP) | Hefesto | grande | issues registradas, P0/P1 corrigidos |
| S6-T08 | Beta fechado: 5 engenheiros usam por 1 semana | Ayla coordena | grande | feedback consolidado |
| S6-T09 | Tag `v0.1.0-beta` | Apolo | pequeno | release notes |
| S6-T10 | Review final Fase 1 | Artemis | médio | parecer go/no-go pra Fase 2 |

---

## SPRINTS 7-13 — Fase 2 (resumo)

| Sprint | Foco | Marco |
|---|---|---|
| S7 | Lajes maciças + nervuradas NBR 6118 | flecha laje ok |
| S8 | Aço NBR 8800 (vigas, pilares, treliça) | dimensionamento perfis tabela |
| S9 | Madeira NBR 7190 + Eurocode 2 (concreto internacional) | |
| S10 | Estaca completa: Décourt-Quaresma, Aoki-Velloso, Teixeira + tubulão refatorado | |
| S11 | Editor PRO (T-20) + override de coeficientes | |
| S12 | Importação IFC 4.x (parser, sem render) + CSV legacy | |
| S13 | Eurocode 3 (aço internacional) + billing Stripe + tier pago | tag `v0.5.0`, fim Fase 2 |

## SPRINTS 14-23 — Fase 3 (resumo)

| Sprint | Foco |
|---|---|
| S14-15 | ACI 318 + AISC 360 |
| S16 | Análise modal + espectro de resposta NBR 15421 / EC8 |
| S17 | Análise não-linear física (concreto fissurado) |
| S18 | Interação solo-estrutura (Winkler) |
| S19 | Recalque por adensamento + adensamento secundário |
| S20 | Exportação DXF planta de fôrma e armação |
| S21 | Tier Studio (multi-usuário, workspace, RBAC granular) |
| S22 | API key + webhooks + plugin Grasshopper (PoC) |
| S23 | Pen test + 30 casos cruzados TQS/SAP2000 + tag `v1.0.0` |

---

## Distribuição de carga por agente (Fase 1)

| Agente | Tasks Fase 1 | Tipo |
|---|---|---|
| Apolo (BE) | ~70 tasks (apos quebras) | implementação backend |
| Íris (FE) | ~12 tasks | wizard, dashboard, relatório |
| Hefesto (QA) | ~10 tasks | fixtures + bench + E2E |
| Artemis (TL) | 6 reviews | revisão de código + arquitetura |
| Atena | ADRs + arquitetura | input pontual |
| Gaia | docs | README, manual, OpenAPI |
| Ayla (PO) | gates + validação | bloqueia release sem evidência |

⚠ Risco: Apolo concentrado em backend pesado. Mitigacao: tasks de infra (S0-T20..T26) podem ser delegadas a Artemis com supervisao Apolo. Buffer 20% por sprint reservado pra fixes.

## Critérios de fim de Fase 1 (gate)

- [ ] Wizard leigo cobre 100% do caso real-alvo (residência uni 1pav, 80m²)
- [ ] Erro vs cálculo de referência (livro) < 1% nos 5 casos canônicos
- [ ] Erro vs TQS em 3 casos práticos < 5%
- [ ] PDF tem citação inline e memória passo-a-passo
- [ ] Pen test sem P0/P1
- [ ] Cobertura `core/` > 80%
- [ ] Beta de 5 engenheiros, NPS médio > 30
- [ ] Tag `v0.1.0-beta` no GitHub
