# _legacy — Arquivo morto

**NÃO importar nada deste diretório em `apps/` ou `core/`.**

Este diretório contém o código original do projeto `lct_calculator` (PyQt6 + SQLite desktop).
Preservado apenas como referência de lógica durante a migração para o stack SaaS (Sprint 0–4).

## Conteúdo

- `src/lct_calculator/calculators/` — 10 classes de cálculo de fundações (sapata, estaca, tubulão, etc.)
- `src/lct_calculator/models/` — entidades de domínio simples (FoundationData, LoadData, ReportData)
- `src/lct_calculator/services/calculation_service.py` — orquestrador legado (quebrado: instancia calculators sem args)
- `src/lct_calculator/interfaces/` — cli.py, report_generator.py (fpdf), tqs_data_importer.py
- `src/lct_calculator/helpers/file_helper.py` — utilitário IO puro
- `src/lct_calculator/database.py` — SQLite síncrono (descartado)

## Destino da migração (Sprint 4)

| Legacy | Destino |
|---|---|
| `calculators/*.py` | `core/foundations/*.py` (refatorado com Pydantic + norma explícita) |
| `models/*.py` | `core/domain/*.py` |
| `interfaces/report_generator.py` | `core/report/pdf_renderer.py` |
| `interfaces/tqs_data_importer.py` | `core/importers/csv_importer.py` + `core/importers/ifc_parser.py` |

**Gate de deleção:** `_legacy/` é deletado em PR único no fim da Sprint 4 após todos os calculators terem:
1. Teste verde com fixture canônica
2. Bench cruzado vs referência bibliográfica (Carvalho/Filho ou Velloso/Lopes) com erro < 1%
3. Aprovação Hefesto
