---
documento: design técnico
versao: 1.0
data: 2026-05-31
status: arquitetura proposta
---

# 03 — DESIGN TÉCNICO

## Stack proposta

### Backend
- **Linguagem**: Python 3.12 (aproveita 100% do código atual)
- **Framework HTTP**: FastAPI 0.110+ (OpenAPI auto, async nativo, type hints)
- **ORM**: SQLAlchemy 2.0 + Alembic (migrations versionadas)
- **DB**: PostgreSQL 16 (multi-tenant, JSONB pra payloads flexíveis)
- **Fila assíncrona**: Celery + Redis (cálculos longos)
- **Cache**: Redis
- **Auth**: FastAPI Users + JWT (refresh + access)

### Motor de cálculo
- **Núcleo numérico**: numpy + scipy (já implícito no código atual)
- **FEM frame**: a definir em WR-002 (fim Sprint 0). Opcoes: (a) implementacao propria, (b) opstool/OpenSeesPy, (c) Pynite. Trade-offs em ADR-0003 (provisional).
- **FEM shell** (lajes): implementação própria simplificada OU integração com `OpenSees` via `openseespy` quando precisar análise não-linear (avaliar v1.5)
- **Geotecnia**: módulo próprio (continuação dos calculators atuais)

### Front (separado, documento próprio depois)
- React + Vite + TypeScript
- shadcn/ui ou Mantine
- TanStack Query pra estado de servidor
- Sem Three.js no MVP

### DevOps
- Docker + docker-compose dev
- GitHub Actions CI: lint + test + build
- Deploy v1: Fly.io ou Railway (custo baixo, fácil)
- Deploy v2: Kubernetes quando pesar (não antes)

### Observabilidade
- Logs: structlog → stdout → coletor cloud (BetterStack/Logtail)
- Métricas: prometheus_client + Grafana Cloud (free tier)
- Erros: Sentry

---

## Arquitetura macro

```
┌──────────────────────────────────────────────────────────┐
│                       Client (web)                        │
└──────────────────────────────────────────────────────────┘
                            │ HTTPS
┌──────────────────────────────────────────────────────────┐
│                 FastAPI (api gateway)                     │
│   - Auth · RBAC · Rate limit · Validation (Pydantic)      │
└──────────────────────────────────────────────────────────┘
       │                    │                     │
       ▼                    ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌──────────────────┐
│  Project svc  │   │  Calc service │   │  Report service  │
│  (CRUD)       │   │ (orquestra)   │   │ (PDF, DXF, IFC)  │
└───────────────┘   └───────────────┘   └──────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │   Celery worker pool     │
              │   (cálculos > 10s)       │
              └─────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│                      core (motor)                         │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐ ┌──────┐ │
│  │  fem   │ │ design │ │  geo   │ │ standards│ │ loads│ │
│  │ (frame)│ │(NBR/EC)│ │(solos) │ │ (normas) │ │      │ │
│  └────────┘ └────────┘ └────────┘ └──────────┘ └──────┘ │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │  PostgreSQL · Redis      │
              └─────────────────────────┘
```

---

## Estrutura de pastas (proposta)

```
calc-3d/
├── apps/
│   ├── api/              # FastAPI HTTP layer
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── schemas/      # Pydantic IO
│   │   ├── deps.py       # auth, db, etc.
│   │   └── middleware/
│   └── worker/           # Celery
│       └── tasks.py
├── core/
│   ├── fem/              # solver
│   │   ├── frame_3d.py
│   │   ├── element.py
│   │   ├── assembler.py
│   │   └── solver.py
│   ├── design/           # dimensionamento por norma
│   │   ├── concrete/
│   │   │   ├── nbr6118.py
│   │   │   ├── eurocode2.py
│   │   │   └── aci318.py
│   │   ├── steel/
│   │   │   ├── nbr8800.py
│   │   │   ├── eurocode3.py
│   │   │   └── aisc360.py
│   │   └── timber/
│   │       └── nbr7190.py
│   ├── geo/              # geotecnia
│   │   ├── soil_profile.py
│   │   ├── bearing_capacity/
│   │   │   ├── terzaghi.py
│   │   │   ├── meyerhof.py
│   │   │   ├── vesic.py
│   │   │   └── brinch_hansen.py
│   │   ├── settlement/
│   │   │   ├── elastic.py
│   │   │   ├── schmertmann.py
│   │   │   └── consolidation.py
│   │   ├── piles/
│   │   │   ├── decourt_quaresma.py
│   │   │   ├── aoki_velloso.py
│   │   │   └── teixeira.py
│   │   └── soil_library.py  # tipos de solo BR
│   ├── foundations/      # ⬅ refatorar calculators atuais aqui
│   │   ├── footing.py
│   │   ├── strip_footing.py
│   │   ├── raft.py
│   │   ├── pile.py
│   │   ├── caisson.py
│   │   └── pile_cap.py
│   ├── loads/            # cargas
│   │   ├── dead.py
│   │   ├── live_nbr6120.py
│   │   ├── wind_nbr6123.py
│   │   ├── seismic_nbr15421.py
│   │   └── combinations_nbr8681.py
│   ├── inference/        # camada simples (mágica)
│   │   ├── cep_to_wind.py
│   │   ├── cep_to_seismic.py
│   │   ├── usage_to_live.py
│   │   └── geometry_inference.py
│   ├── standards/        # versionamento de norma
│   │   └── registry.py
│   ├── report/           # PDF, DXF
│   │   ├── pdf_renderer.py
│   │   └── dxf_writer.py
│   ├── importers/        # IFC parser, CSV, JSON
│   │   ├── ifc_parser.py     # ifcopenshell SEM .geom
│   │   ├── csv_importer.py
│   │   └── json_importer.py
│   └── domain/           # entidades puras
│       ├── project.py
│       ├── element.py
│       ├── material.py
│       └── result.py
├── infra/
│   ├── db/
│   │   └── migrations/   # alembic
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   └── deploy/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── fixtures/         # casos canônicos por norma
│   └── benchmarks/       # comparação cruzada com TQS/SAP2000
├── docs/
│   ├── planning/         # ⬅ você está aqui
│   ├── manual/           # manual técnico
│   └── adr/              # decisões arquiteturais
├── pyproject.toml
└── README.md             # ⬅ reescrever
```

**Migração do código atual:**
- `src/lct_calculator/calculators/*.py` → `core/foundations/*.py` (refatora pra nova interface)
- `src/lct_calculator/models/*.py` → `core/domain/*.py`
- `src/lct_calculator/services/calculation_service.py` → orquestrador novo em `apps/api/services/`
- `src/lct_calculator/services/sqlite_service.py` → **descarta** (vamos pra Postgres + SQLAlchemy)
- `src/lct_calculator/interfaces/*.py` → **descarta** (PyQt6 sai todo)
- `src/lct_calculator/interfaces/tqs_data_importer.py` → `core/importers/csv_importer.py` + `ifc_parser.py`
- `src/lct_calculator/interfaces/report_generator.py` → `core/report/pdf_renderer.py`

---

## Versionamento de API

Todos os endpoints sob /api/v1/... desde Sprint 0. Politica de deprecation: header `Deprecation: true` + `Sunset: <RFC 1123 date>` quando endpoint sair. Bump major (v2) so para breaking changes de contrato. Documentado em ADR-0006 (a criar).

## Idempotencia de cálculo

POST /api/v1/projects/{id}/calculate aceita header `Idempotency-Key` (opcional, gerado pelo client). Servidor mantem chave no Redis por 24h. Internamente, hash SHA-256 do snapshot canonico (projeto + standards_config + engine_version) e a chave estavel: cache_hit retorna calc_result existente sem reprocessar. Race condition mitigada via INSERT ON CONFLICT no audit_log com (project_id, payload_hash) UNIQUE.

## Contrato de violacao normativa

Todo calculator que falha em check normativo retorna instancia de:

```python
class NormativeViolation:
    code: str            # ex "NBR-6118-17.3.5.2.1"
    standard_ref: str    # ex "NBR 6118:2014 §17.3.5.2.1"
    formula: str         # ex "ρ_min = 0.15%"
    actual: float        # 0.0008
    limit: float         # 0.0015
    severity: Literal["error", "warning", "info"]
    suggestion: str      # ex "Aumentar As para 4 ø 12.5 ou reduzir b para 18cm"
```

Serializa direto pro JSON da resposta e alimenta a UI T-30. Calculators NUNCA inventam formato proprio.

## Multi-tenancy: SQLAlchemy + asyncpg + RLS

Mecanismo concreto:
1. Middleware FastAPI extrai `tenant_id` do JWT.
2. Dependency injeta na sessao SQLAlchemy via `session.info["tenant_id"]`.
3. Event listener `do_orm_execute` (SQLAlchemy 2 async) executa `SET LOCAL app.tenant_id = :tid` na conexao antes de cada query.
4. Connection pool: `pool_reset_on_return='rollback'` garante reset entre requests.
5. Todas as tabelas com tenant scope tem POLICY `USING (tenant_id::text = current_setting('app.tenant_id'))`.
6. Teste adversarial em S1-T04: criar 2 tenants, query do tenant A retorna 0 rows do tenant B.

## Estrategia de migracao do legado

`src/lct_calculator/` permanece intocado em `_legacy/` (movido em S0-T14, NAO importado por apps/api). Cada calculator de `core/foundations/` so substitui o legacy quando: (a) tem teste verde com fixture canonica, (b) bench cruzado vs Carvalho/Filho ou Velloso/Lopes passa, (c) Hefesto aprova. Deletar `_legacy/` em PR unico no fim da Sprint 4 (gate Fase 1).

## Custo operacional estimado (mensal)

Tier dev (Fase 0-1):
- Fly.io: API + worker + Postgres managed + Redis = ~US$ 30-60
- Sentry, BetterStack: free tier
- GitHub Actions: free tier
- Total: ~US$ 30-80/mes

Tier prod (Fase 2 release):
- Fly.io tier pago: 2x API instance + worker + Postgres High Availability + Redis Persistent + storage = ~US$ 150-300
- Total: ~US$ 200/mes

Alerta de billing em US$ 100 (dev) / US$ 400 (prod). Politica quando estourar quota: throttle automatico de tier Free + email pra admin.

---

## Modelos de domínio (esboço)

```python
# core/domain/project.py
class Project:
    id: UUID
    tenant_id: UUID
    name: str
    cep: str | None       # alimenta inference
    usage_type: UsageType  # alimenta carga acidental
    standards: StandardsConfig  # qual norma + versão aplicar

# core/domain/element.py
class StructuralElement:
    id: UUID
    project_id: UUID
    type: ElementType  # beam, column, slab, footing...
    material: Material
    geometry: Geometry
    supports: list[Support]
    loads: list[LoadCase]

# core/domain/material.py
class Material:
    type: MaterialType  # concrete, steel, timber
    grade: str          # C25, A572, etc.
    properties: MaterialProperties  # E, fy, fck, γ, ...

# core/geo/soil_profile.py
class SoilLayer:
    depth_top: float
    depth_bottom: float
    soil_type: SoilType
    properties: SoilProperties  # γ, c, φ, NSPT, qc, ...

class SoilProfile:
    layers: list[SoilLayer]
    water_table_depth: float
```

---

## Fluxo: cálculo via wizard leigo

```
1. POST /projects (cep, usage_type, geometry_simplified)
2. core/inference roda:
   - cep_to_wind(cep) → vb, V0
   - usage_to_live(usage_type) → carga acidental NBR 6120
   - geometry_inference(planta, pavimentos) → grid de pilares default
3. POST /projects/{id}/calculate
4. apps/api enfileira em Celery se cálculo > 10s
5. worker chama core/fem + core/design + core/geo
6. resultado salvo, webhook/notification dispara
7. GET /projects/{id}/report → PDF
```

## Fluxo: cálculo via API pro

```
1. POST /projects (config completa, override de coeficientes)
2. POST /projects/{id}/elements (lote — nós, barras, materiais)
3. POST /projects/{id}/calculate
4. mesmo backend, sem inferência (tudo veio explícito)
```

---

## Multi-tenancy

- **Estratégia**: `tenant_id` em toda tabela + Row Level Security no Postgres
- Cada projeto pertence a 1 tenant
- API filtra automaticamente via middleware (`current_user.tenant_id`)
- Auditoria: log de query cross-tenant é alarme P0

---

## Versionamento de norma

```python
# core/standards/registry.py
class Standard:
    code: str        # "NBR-6118"
    edition: str     # "2014"
    valid_from: date
    valid_to: date | None

# escolha por projeto:
project.standards = {
    "concrete": "NBR-6118:2014",
    "steel": "NBR-8800:2008",
    "wind": "NBR-6123:1988",
}
```

Cada cálculo registra qual versão de norma aplicou. Atualização de norma = nova versão do módulo, antigos não são afetados.

---

## Decisões arquiteturais (ADRs a documentar)

1. **ADR-001**: Por que FastAPI + Python (vs Rust/.NET) — aproveita código atual, ecossistema científico
2. **ADR-002**: Por que sem 3D no MVP — custo de UX vs valor real, foco em precisão
3. **ADR-003-DRAFT (provisional)**: Motor FEM — escolha pendente WR-002 (fim Sprint 0). Opcoes em avaliacao: (a) motor proprio, (b) opstool/OpenSeesPy, (c) Pynite. Atualizar pra ADR-0003 final apos WR-002.
4. **ADR-004**: Por que multi-tenant via tenant_id (vs schema-per-tenant) — escala, simplicidade ops
5. **ADR-005**: Por que Postgres (vs MongoDB) — transações, JSONB cobre flexibilidade, integridade referencial
6. **ADR-006**: Versionamento de API (/api/v1) e politica de deprecation
7. **ADR-007**: Push real-time pra status de calculo (WS vs SSE vs polling — decidir em ADR antes de S5)
