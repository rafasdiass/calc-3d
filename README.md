# calc-3d

> Plataforma SaaS de cálculo estrutural de fundações — API multi-tenant com FastAPI, Celery e PostgreSQL.

---

## Visão geral

**calc-3d** é uma API REST para dimensionamento de fundações (sapatas, estacas, radiers, blocos, tubulões, etc.) com suporte a:

- Multi-tenancy via JWT (`tenant_id` claim)
- Cálculos assíncronos via Celery + Redis
- Persistência em PostgreSQL (asyncpg + SQLAlchemy 2.x)
- Exportação de relatórios (PDF, JSON, CSV) — Sprint 2
- Integração TQS/IFC — Sprint 2

---

## Stack

| Camada | Tecnologia |
|---|---|
| API | FastAPI 0.111 + Uvicorn |
| Schemas | Pydantic v2 |
| Auth | JWT (python-jose) + Argon2 (passlib) |
| Worker | Celery 5 + Redis |
| DB | PostgreSQL 16 + asyncpg + SQLAlchemy 2 |
| Migrations | Alembic |
| Testes | pytest + pytest-asyncio + httpx |
| Linting | Ruff + Mypy (strict) |

---

## Estrutura

```
calc-3d/
├── apps/
│   ├── api/          ← FastAPI app (routers, schemas, middleware)
│   └── worker/       ← Celery tasks
├── core/
│   ├── domain/       ← entidades de domínio (Sprint 1)
│   ├── fem/          ← módulo FEM (Sprint 2)
│   ├── design/       ← verificações NBR (Sprint 2)
│   ├── geo/          ← geometria 3D (Sprint 2)
│   └── utils/        ← utilitários compartilhados
├── infra/
│   ├── db/           ← sessão async SQLAlchemy
│   ├── cache/        ← cliente Redis
│   └── storage/      ← cliente S3-compatible
├── tests/
│   ├── unit/
│   └── integration/
└── _legacy/          ← código legado preservado (referência para Sprint 1)
```

---

## Quickstart

```bash
# 1. Instalar dependências
pip install -e ".[dev]"

# 2. Configurar variáveis de ambiente
cp .env.example .env
# editar .env com DATABASE_URL, SECRET_KEY, REDIS_URL

# 3. Rodar API
uvicorn apps.api.main:app --reload --port 8000

# 4. Rodar worker Celery
celery -A apps.worker.tasks.celery_app worker --loglevel=info

# 5. Rodar testes
pytest --cov=apps --cov=core --cov-report=term-missing
```

---

## Endpoints Sprint 0

| Método | Path | Auth | Descrição |
|---|---|---|---|
| GET | `/api/health` | ❌ | Health check |
| POST | `/api/auth/register` | ❌ | Registrar usuário |
| POST | `/api/auth/token` | ❌ | Obter JWT |

Documentação interativa: `http://localhost:8000/api/docs`

---

## Roadmap

- **Sprint 0** ✅ — Scaffolding, FastAPI, auth stubs, CI/CD base
- **Sprint 1** — Domínio fundações, PostgreSQL, auth real, CRUD projetos
- **Sprint 2** — Cálculos NBR, FEM, exportação, integração TQS/IFC
- **Sprint 3** — Visualização 3D, dashboard, multi-tenant billing

---

## Legado

O diretório `_legacy/` contém o código original (Python puro, PyQt6) preservado como referência para migração das lógicas de cálculo para `core/`.
