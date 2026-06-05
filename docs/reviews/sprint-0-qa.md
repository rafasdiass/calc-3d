---
documento: QA Report — Sprint 0 (parcial)
versao: 1.0
data: 2026-06-05
autor: Artemis (QA phase — pipeline task-2e6d6464)
sprint: S0
status: PARTIAL PASS — bloqueadores presentes
---

# QA Report — Sprint 0 (parcial)

> Escopo: avaliar o que foi implementado na fase que o executor anterior identificou como
> "FASE 2 — Criar estrutura de pastas (S0-T05)". Varredura cobre todos os tasks S0-T01..T05
> que dependiam apenas de operações de filesystem + git (sem infraestrutura Docker/CI/Auth).

---

## Resumo executivo

| Resultado | Tasks |
|---|---|
| ✅ PASS | S0-T01, S0-T02, S0-T14, S0-T15, PRE-FLIGHT blockers A1/A2/A3/A4 |
| ⚠️ PASS com ressalva | S0-T03 |
| ❌ FAIL | S0-T04, S0-T05 |
| ⏳ Fora de escopo QA agora | S0-T06..T13, T16..T28 (requerem Docker, CI, PostgreSQL, Redis) |

**Veredito geral: 🔴 BLOQUEADO para release de S0** — estrutura de pastas não bate com `03-DESIGN.md`, `pyproject.toml` ausente, e a árvore correta (`apps/`, `core/`, `infra/`) não foi criada.

---

## Checks individuais

### ✅ CHECK-01 — S0-T01: Deletar arquivos descartáveis

**DoD**: `git diff` confirma remoção de `simple_calculator.py`,
`interfaces/foundation_calculator_interface.py`, `interfaces/visualizador_ifc.py`, `main.py`,
`sqlite_service.py`, arquivos `.DS_Store`.

**Resultado: PASS**

Evidência (commit `af58188`):
```
chore(cleanup): remover GUI PyQt6, viewer 3D, sqlite_service, simple_calculator
- src/lct_calculator/calculators/simple_calculator.py  (169 linhas)
- src/lct_calculator/interfaces/__init__.py            (13 linhas)
- src/lct_calculator/interfaces/foundation_calculator_interface.py (251 linhas)
- src/lct_calculator/interfaces/visualizador_ifc.py    (133 linhas)
- src/lct_calculator/main.py                           (22 linhas)
- src/lct_calculator/services/sqlite_service.py        (55 linhas)
Total: 643 linhas removidas.
```
Nenhum `.DS_Store` rastreado encontrado no working tree.

---

### ✅ CHECK-02 — S0-T02: Atualizar `.gitignore`

**DoD**: `.gitignore` deve conter `.DS_Store`, `__pycache__/`, `.idea/`, `venv/`, `.env*`.

**Resultado: PASS**

`.gitignore` verificado — todas as entradas presentes:
```
.DS_Store / **/.DS_Store   ✅
__pycache__/               ✅
.idea/                     ✅
venv/ / .venv/ / env/      ✅
.env / .env.*              ✅
docs/private/              ✅ (bônus: S0-T27 antecipado)
```

---

### ⚠️ CHECK-03 — S0-T03: Reescrever README.md

**DoD**: README deve descrever escopo backend SaaS, sem PySide2/PyQt6. Review Ayla pendente.

**Resultado: PASS parcial (conteúdo não atualizado)**

O `README.md` no repositório ainda descreve o projeto como aplicação desktop:
> "LCT Calculator é um projeto desenvolvido para calcular diferentes tipos de fundações...
> **Sincronização com Plataforma BIM**... **Pyside2**: Para a criação da interface gráfica."

O README continua referenciando SQLite, PyQt/PySide2, `bim_integration.py`. Nada sobre FastAPI,
PostgreSQL, multi-tenant ou SaaS. Este task **não foi executado**. Não bloqueia S0 gate
tecnicamente (DoD inclui "review Ayla"), mas é dívida visível e inconsistência de comunicação.

**Ação requerida**: Gaia/Apolo reescrever README antes do gate de S0.

---

### ❌ CHECK-04 — S0-T04: Criar `pyproject.toml`

**DoD**: arquivo presente, `pip install -e .` funciona. Deve declarar Python 3.12, FastAPI,
SQLAlchemy 2, Alembic, Pydantic 2, Celery, Redis, ruff, mypy, pytest.

**Resultado: FAIL — arquivo inexistente**

`find` não encontrou nenhum `pyproject.toml` no repositório. Existe apenas o `setup.py` legado
(referencia `lct_calculator.main:main`, declara `numpy` e `pandas` — ambos irrelevantes para a
nova stack).

Stack alvo (FastAPI, SQLAlchemy 2, Alembic, Pydantic v2, Celery, Redis, ruff, mypy) **não está
declarada em nenhum arquivo de configuração**.

**Impacto**: S0-T07 (FastAPI hello world), S0-T08 (Alembic), S0-T10 (Auth), S0-T12 (CI) — todos
dependem de `pyproject.toml`. Gate Marco do Sprint 0 (`curl localhost:8000/health → 200`) está
bloqueado.

---

### ❌ CHECK-05 — S0-T05: Layout de pastas conforme `03-DESIGN.md`

**DoD**: árvore conforme `03-DESIGN.md` — `apps/api/`, `core/`, `infra/`, `tests/unit/` etc.

**Resultado: FAIL — layout incorreto (namespace errado)**

Layout esperado por `03-DESIGN.md`:
```
calc-3d/
├── apps/
│   ├── api/  (routers/, schemas/, middleware/, main.py, deps.py)
│   └── worker/
├── core/
│   ├── fem/  ├── design/  ├── geo/  ├── foundations/
│   ├── loads/  ├── inference/  ├── standards/
│   ├── report/  ├── importers/  └── domain/
├── infra/
│   ├── db/migrations/  ├── docker/  └── deploy/
└── tests/
    ├── unit/  ├── integration/  ├── fixtures/  └── benchmarks/
```

Layout encontrado:
```
calc-3d/
├── src/
│   └── lct_calculator/
│       ├── calculators/   (VAZIO — namespace legado)
│       ├── helpers/       (VAZIO — namespace legado)
│       ├── interfaces/    (VAZIO — namespace legado)
│       ├── models/        (VAZIO — namespace legado)
│       └── services/      (VAZIO — namespace legado)
├── _legacy/lct_calculator/ (legado isolado — ✅ correto, S0-T14)
└── tests/                  (sem subdirs unit/integration/fixtures/benchmarks)
```

**Diagnóstico**: o executor criou subpastas dentro de `src/lct_calculator/` — que replica
exatamente a estrutura do legado, não a estrutura nova do `03-DESIGN.md`. O task foi
executado no namespace errado. `apps/`, `core/` e `infra/` não existem.

**Gaps críticos**:
- `apps/` — ausente
- `core/` — ausente
- `infra/` — ausente
- `tests/unit/`, `tests/integration/`, `tests/fixtures/`, `tests/benchmarks/` — ausentes
- `src/lct_calculator/` residual com 5 pastas vazias (polui a árvore, deve ser removido)

---

### ✅ CHECK-06 — S0-T14: Isolar legado em `_legacy/`

**DoD**: código legado movido para `_legacy/`, não importado por `apps/api`.

**Resultado: PASS**

Commit `476316b` move todo `src/lct_calculator/` → `_legacy/lct_calculator/`. Nenhum import
cruzado detectado (não existe `apps/api/` que possa importar `_legacy`). Legado está isolado
e intacto, conforme design de migração gradual definido em `03-DESIGN.md`.

---

### ✅ CHECK-07 — S0-T15: ADRs em `docs/adr/`

**DoD**: ADR-001, ADR-002, ADR-005 (mínimo). ADR-003 marcada `provisional`.

**Resultado: PASS**

5 ADRs presentes e com conteúdo substantivo:
- `docs/adr/0001-stack-backend-python-fastapi.md` — status: `accepted` ✅
- `docs/adr/0002-sem-3d-no-mvp.md` — presente ✅
- `docs/adr/0003-motor-fem.md` — status: `provisional` ✅ (correto, aguarda WR-002)
- `docs/adr/0004-multi-tenancy-tenant-id-rls.md` — presente ✅
- `docs/adr/0005-postgres-alembic-jsonb.md` — presente ✅

---

### ✅ CHECK-08 — PRE-FLIGHT blockers: A1, A2, A3, A4

**Resultado: PASS**

| Bloqueador PRE-FLIGHT | Artefato esperado | Encontrado |
|---|---|---|
| A1 — Hermes scan | `docs/scans/2026-05-31-baseline-calc-3d.json` | ✅ presente, inventário completo |
| A2 — ADRs Atena | `docs/adr/*.md` (5 ADRs) | ✅ 5 arquivos |
| A3 — Despacho Hera | `docs/dispatches/2026-05-31-planning-v1.md` | ✅ presente, V-FLIGHT registrado |
| A4 — WR-001 ata | `docs/debates/WR-001-aprovacao-planning.md` | ✅ 5/5 APPROVE_WITH_CHANGES |

---

### ✅ CHECK-09 — Teste de regressão

**Resultado: PASS**

```
python3 -m unittest discover -s tests -v
test_example (test_lct_calculator.TestLCTCalculator.test_example) ... ok
Ran 1 test in 0.000s — OK
```

Único teste existente (`1+1==2`) passa. Os demais arquivos de teste
(`test_foundation_calculator.py`, `test_report_generator.py`, `test_tqs_data_importer.py`)
estão vazios — nenhuma regressão, nenhum falso positivo.

---

### ✅ CHECK-10 — Git history / commits atomizados

**Resultado: PASS**

```
476316b  chore(legacy): isolar código legado em _legacy/ (S0-T14)
af58188  chore(cleanup): remover GUI PyQt6, viewer 3D, sqlite_service, simple_calculator (S0-T01)
080e432  chore: add olimpo.yaml
a9751a4  docs(planning): planning v1 — pivot calc-3d → backend SaaS
```

Commits são semânticos, atômicos, rastreáveis.

---

## Mapa de gaps vs DoD Sprint 0

| Task | Descrição | Status | Bloqueador para gate? |
|---|---|---|---|
| S0-T01 | Deletar descartáveis | ✅ DONE | — |
| S0-T02 | `.gitignore` atualizado | ✅ DONE | — |
| S0-T03 | README reescrito | ⚠️ PENDENTE | Soft block |
| S0-T04 | `pyproject.toml` | ❌ AUSENTE | 🔴 Bloqueia S0-T07/T08/T10/T12 |
| S0-T05 | Layout `apps/core/infra/tests` | ❌ NAMESPACE ERRADO | 🔴 Bloqueia toda implementação nova |
| S0-T06 | Docker + compose | ⏳ Não iniciado | Depende de S0-T04/T05 |
| S0-T07 | FastAPI `/health` | ⏳ Não iniciado | Depende de S0-T04/T05 |
| S0-T08..T13 | Alembic, Auth, CI, Observabilidade | ⏳ Não iniciado | Depende de S0-T04/T05 |
| S0-T14 | Legado em `_legacy/` | ✅ DONE | — |
| S0-T15 | ADRs documentados | ✅ DONE | — |
| S0-T16..T28 | Frontend, E2E, hardening, extras | ⏳ Fora de escopo desta fase | — |

---

## Ações bloqueadoras (próximo executor deve resolver antes de continuar)

### 🔴 BLOCK-1 — Criar `pyproject.toml` (S0-T04)

Arquivo mínimo esperado (exemplo):

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "calc-engine"
version = "0.0.1"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.110",
    "uvicorn[standard]>=0.29",
    "sqlalchemy>=2.0",
    "alembic>=1.13",
    "pydantic>=2.0",
    "pydantic-settings>=2.0",
    "celery>=5.3",
    "redis>=5.0",
    "asyncpg>=0.29",
    "python-jose[cryptography]>=3.3",
    "passlib[bcrypt]>=1.7",
    "httpx>=0.27",
    "structlog>=24.0",
    "prometheus-client>=0.20",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "pytest-cov>=5.0",
    "ruff>=0.4",
    "mypy>=1.10",
    "types-redis",
]

[tool.ruff]
target-version = "py312"
line-length = 100

[tool.mypy]
python_version = "3.12"
strict = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
```

**Owner**: Apolo.

### 🔴 BLOCK-2 — Recriar layout de pastas correto (S0-T05)

```bash
# 1. Remover src/ residual (vazio, legado já está em _legacy/)
rm -rf src/

# 2. Criar estrutura conforme 03-DESIGN.md
mkdir -p apps/api/{routers,schemas,middleware}
touch apps/api/main.py apps/api/deps.py
mkdir -p apps/worker
touch apps/worker/tasks.py
mkdir -p core/{fem,foundations,loads,inference,standards,report,importers}
mkdir -p core/design/{concrete,steel,timber}
mkdir -p core/geo/{bearing_capacity,settlement,piles}
mkdir -p core/domain
mkdir -p infra/db/migrations infra/docker infra/deploy
mkdir -p tests/{unit,integration,fixtures,benchmarks}

# 3. __init__.py nos pacotes Python
find apps core -type d | xargs -I{} touch {}/__init__.py
touch tests/__init__.py
```

**Owner**: Apolo.

### ⚠️ WARN-1 — README desatualizado (S0-T03)

Reescrever descrevendo: SaaS multi-tenant, backend FastAPI, motor FEM, PostgreSQL.
Remover toda referência a PyQt/PySide2/SQLite/BIM-sync.
**Owner**: Gaia.

### ⚠️ WARN-2 — `setup.py` legado ainda presente

`setup.py` referencia `lct_calculator.main:main` (entry point removido). Após criar
`pyproject.toml`, remover `setup.py` para evitar conflito de build.
**Owner**: Apolo.

---

## O que está sólido (não tocar)

- Processo Olimpo seguido: PRE-FLIGHT, WR-001 (5 votos), despacho Hera, scan Hermes — todos presentes.
- Limpeza de legado (S0-T01): 643 linhas de GUI removidas, sem perda de calculadoras de domínio.
- `.gitignore` correto e abrangente.
- 5 ADRs com conteúdo real; ADR-003 `provisional` alinhado ao WR-002 pendente.
- Legado isolado em `_legacy/` sem imports cruzados.
- Git history limpo e semântico.

---

## Marco gate S0

> `curl localhost:8000/health → 200` + signup/login + CI verde

**Status: 🔴 BLOQUEADO**

Dependências diretas do gate:
1. `pyproject.toml` → instala FastAPI, cria ambiente reproduzível
2. `apps/api/main.py` com `/health` → requer estrutura `apps/`
3. `infra/docker/docker-compose.yml` → requer `infra/`
4. CI GitHub Actions → requer `pyproject.toml` com ruff/mypy/pytest

Nenhum destes pode ser criado enquanto BLOCK-1 e BLOCK-2 estiverem abertos.

---

*QA executado por Artemis — pipeline task-2e6d6464 — 2026-06-05T04:31:35Z*
