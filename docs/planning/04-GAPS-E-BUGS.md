---
documento: gaps, bugs e dívida técnica
versao: 1.0
data: 2026-05-31
fonte: auditoria de código (branch installer, idêntico a main exceto .DS_Store + arquivo vazio "cmaker")
---

# 04 — GAPS, BUGS E DÍVIDA TÉCNICA

## A. Arquivos descartáveis (devem sair em Sprint 0)

| Arquivo | Motivo |
|---|---|
| `src/lct_calculator/cmaker` | arquivo vazio sem propósito (commit "cmaker" da branch installer) |
| `src/lct_calculator/interfaces/foundation_calculator_interface.py` | janela PyQt6 + Qt3D — descarte total (251 linhas) |
| `src/lct_calculator/interfaces/visualizador_ifc.py` | viewer 3D IFC — descarte total (133 linhas) |
| `src/lct_calculator/main.py` | só dispara QApplication, vai ser substituído por entrypoint FastAPI |
| `.DS_Store` (todos) | lixo macOS — adicionar ao .gitignore |
| `installer/cmaker` | placeholder vazio |

**Total a deletar: ~400 linhas + 4 arquivos binários**

## B. Arquivos a refatorar (ficam, mas mudam de lugar/contrato)

| Arquivo atual | Vai virar | Motivo |
|---|---|---|
| `calculators/sapata.py` | `core/foundations/footing.py` | renome inglês, refatora interface, adiciona Terzaghi/Meyerhof |
| `calculators/estaca.py` | `core/foundations/pile.py` | adicionar Décourt-Quaresma, Aoki-Velloso |
| `calculators/sapata_corrida.py` | `core/foundations/strip_footing.py` | mesmo tratamento |
| `calculators/radier.py` | `core/foundations/raft.py` | precisa molas Winkler |
| `calculators/bloco.py` | `core/foundations/pile_cap.py` | NBR 6118 punção |
| `calculators/barrete.py` | `core/foundations/barrette.py` | refinar |
| `calculators/estaca_helice_continua.py` | `core/foundations/cfa_pile.py` | refinar |
| `calculators/tubulão.py` + variantes | `core/foundations/caisson*.py` | unificar API |
| `calculators/simple_calculator.py` | **deletar** | calculadora financeira não pertence a esse produto |
| `models/foundation_data.py` | `core/domain/element.py` (parte) | virar entidade rica, não dict |
| `models/load_data.py` | `core/loads/case.py` | refatora |
| `models/report_data.py` | `core/report/output.py` | refatora |
| `services/calculation_service.py` | `apps/api/services/calculator.py` | refatora pra orquestrar via Celery |
| `services/sqlite_service.py` | **deletar** | vai pra Postgres + SQLAlchemy |
| `services/bim_integration.py` | `apps/api/services/bim_sync.py` | hoje é stub vazio, virar webhook real |
| `interfaces/tqs_data_importer.py` | `core/importers/csv_importer.py` + `core/importers/ifc_parser.py` | dividir em dois (CSV puro + IFC metadata) |
| `interfaces/report_generator.py` | `core/report/pdf_renderer.py` | manter lógica, mover de pacote |
| `interfaces/cli.py` | `apps/cli/main.py` | manter como ferramenta de dev/debug, opcional |
| `database.py` | `infra/db/legacy_schema.py` (descartar após migration) | esquema atual usa JSON stringify, vamos pra colunas tipadas |

## C. Bugs e problemas reais identificados

### B-001 (P1) — README desatualizado
- README.md afirma "PySide2", código real usa PyQt6
- **Impacto**: usuário novo não consegue instalar
- **Fix**: reescrever README pro novo escopo (parte da Sprint 0)

### B-002 (P2) — Encoding de nome de arquivo
- `tubulão.py`, `tubulão_ar_comprimido.py`, `tubulão_ceu_aberto.py` têm acento em nome de arquivo
- **Impacto**: import quebra em sistemas com locale não-UTF-8
- **Fix**: renomear pra `caisson*.py` (já entra na refatoração)

### B-003 (P1) — Persistência insegura
- `services/sqlite_service.py` guarda `dados_entrada` e `resultado` como JSON stringify
- **Impacto**: zero capacidade de query por propriedade, zero validação de schema, dado não migrável
- **Fix**: schema relacional + JSONB tipado em Postgres

### B-004 (P2) — Falta de validação de input
- Calculadores assumem que input é número positivo, sem checar
- Ex: `Sapata(carga=-100, fck=0)` retorna divisão por zero ou número absurdo
- **Fix**: Pydantic schemas no boundary

### B-005 (P0 conceitual) — Normas implícitas
- Sapata calcula "armadura mínima de 0,15%" — comentário menciona NBR 6118 mas não há rastreabilidade
- **Impacto**: impossível auditar, impossível atualizar pra nova versão da norma
- **Fix**: classe `NBR6118` com método `min_reinforcement_ratio(element_type, fck) -> float` e citação inline

### B-006 (P1) — Sem testes
- `tests/` existe mas é vazia/stub
- **Impacto**: refatorar é cego, regressão silenciosa
- **Fix**: pytest + fixtures de casos canônicos antes de tocar nos calculators

### B-007 (P2) — Hardcoded em português
- Strings, nomes de variável, mensagens de erro — tudo em PT
- **Impacto**: i18n futura inviável
- **Fix**: código em inglês, mensagens user-facing em PT (i18n via gettext ou similar)

### B-008 (P0) — Acoplamento solo-fundação ausente
- Cada calculador de fundação recebe `tensao_admissivel_solo` ou `capacidade_solo` como **número solto**
- Não há tipo Solo nem perfil estratigráfico
- **Impacto**: usuário precisa pré-calcular capacidade fora do sistema → derruba o ponto central do produto
- **Fix**: módulo `core/geo/` completo (parte da Sprint 1)

### B-009 (P1) — Sem versionamento de norma
- Toda fórmula está hardcoded com valores da NBR 6118:2014 (presumido)
- **Impacto**: quando NBR for atualizada, fork no código todo
- **Fix**: registry de norma versionada

### B-010 (P2) — Sem auditoria
- Nenhum log de quem calculou, quando, com qual versão
- **Impacto**: impossível responder a questionamento técnico/jurídico
- **Fix**: tabela `calc_audit_log` imutável

### B-011 (P1) — Sem multi-tenancy
- SQLite local, single-user
- **Impacto**: impossível virar SaaS sem reescrita de persistência
- **Fix**: Postgres + `tenant_id` em toda tabela + RLS

## D. Gaps de domínio (o que falta de cálculo de verdade)

### Geotecnia
- ❌ Capacidade de carga teórica (Terzaghi, Meyerhof, Vesic, Brinch-Hansen) — só usa input de capacidade pronto
- ❌ Recalque (elástico, Schmertmann, adensamento)
- ❌ Correlações SPT (Décourt-Quaresma, Aoki-Velloso) — entradas estão lá mas fórmula não confere com norma
- ❌ Tipos de solo (não tem `argila_mole`, `areia_compacta` — só número)
- ❌ Perfil estratigráfico
- ❌ Nível d'água
- ❌ Interação solo-estrutura (molas Winkler)

### Estrutural
- ❌ Análise estrutural (FEM frame 3D) — não tem nada, só fundação isolada
- ❌ Vigas, pilares, lajes — zero código
- ❌ Combinações de carga (NBR 8681)
- ❌ Vento (NBR 6123) — campo `vento` nem existe no input
- ❌ Sismo (NBR 15421)
- ❌ Aço, madeira — zero
- ❌ Verificações ELS (flecha, fissuração)

### Cargas
- ❌ Inferência por tipo de uso (NBR 6120)
- ❌ Mapa de vento por CEP
- ❌ Composição de cargas em pavimentos múltiplos

### Saídas
- ❌ Memória de cálculo passo-a-passo (PDF gera tabela mas sem rastreio de fórmula)
- ❌ Citação inline de norma
- ❌ Lista de materiais
- ❌ DXF
- ❌ IFC export (só import)

## E. Validações pendentes (research em background)

Estes itens foram VALIDADOS pelo workflow deep-research wf_027b7cf1-111 (concluido 2026-05-31). Resultado consolidado em `10-RESEARCH-COMPETITIVO.md`. 23 claims confirmadas adversarialmente, 2 refutadas. Principais validacoes: (a) gap competitivo SaaS+NBR+multi-material+multi-solo confirmado, (b) Eberick nao lista madeira oficialmente, (c) opstool/OpenSeesPy emergiu como motor open-source viavel, (d) faixa de pricing R$ 100-300/mes confirmada como ordem de grandeza abaixo de Eberick.

## F. Resumo numérico

| Métrica | Valor |
|---|---|
| Linhas no projeto atual | 2.688 |
| Linhas a deletar (3D/GUI/lixo) | ~500 |
| Linhas a refatorar e migrar | ~1.500 |
| Linhas zona cinza | ~166 |
| Linhas a escrever do zero (FEM + design + geo + cargas + inference) | estimado 15.000-25.000 |
| ⚠ Caveat | estimativa assume motor FEM proprio. Se WR-002 (fim Sprint 0) escolher opstool/OpenSeesPy, faixa cai para 8-15k linhas (motor reusado, foco em normas + integracao). |
| Cobertura de testes atual | 0% |
| Bugs P0 identificados | 2 |
| Bugs P1 identificados | 4 |
| Bugs P2 identificados | 4 |
| Gaps de domínio críticos | ~25 |
