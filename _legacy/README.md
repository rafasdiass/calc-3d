# _legacy/

Código legado arquivado — **não importar em `apps/` ou `core/`**.

| Pasta | Origem | Migra para |
|---|---|---|
| `calculators/` | `src/lct_calculator/calculators/` | `core/foundations/` — Sprint 4 |
| `models/` | `src/lct_calculator/models/` | `core/domain/` — Sprint 1 |
| `services/` | `src/lct_calculator/services/calculation_service.py` | `apps/api/services/` — Sprint 1 |
| `interfaces/` | `src/lct_calculator/interfaces/` (tqs, report, cli) | `core/importers/`, `core/report/`, `apps/cli/` |
| `helpers/` | `src/lct_calculator/helpers/` | avaliar reuso |

**Deletar em PR único ao fim da Sprint 4.** Gate: Hefesto aprova.
