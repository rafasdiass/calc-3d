---
documento: roadmap
versao: 1.0
data: 2026-05-31
horizonte: 12 meses (junho/2026 → maio/2027)
---

# 05 — ROADMAP

## Visão de longo prazo

```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│   FASE 0     │   FASE 1     │   FASE 2     │   FASE 3     │
│  FUNDAÇÃO    │ MVP CONCRETO │ MVP COMPLETO │   v1.0 GA    │
├──────────────┼──────────────┼──────────────┼──────────────┤
│  jun-jul/26  │  ago-set/26  │  out-dez/26  │  jan-mai/27  │
│  6 semanas   │  8 semanas   │  12 semanas  │  20 semanas  │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

---

## Fase 0 — Fundação técnica (6 semanas)

**Objetivo**: arrancar lixo, instalar fundação, ter "hello world" rodando.

**Entregas**:
- Repo limpo (sem PyQt6, sem cmaker, sem .DS_Store, sem 3D)
- Esqueleto FastAPI rodando em Docker
- Postgres + Alembic configurados
- CI verde (lint, type, test)
- README reescrito
- 1 endpoint de health check
- Auth básica (signup/login/JWT)

**Não-objetivo**: nenhum cálculo real ainda.

**Sucesso**: `curl localhost:8000/health` retorna 200.

---

## Fase 1 — MVP Concreto (Brasil, sapata + viga + pilar) (8 semanas)

**Objetivo**: o **menor produto utilizável** que cobre um caso real ponta-a-ponta.

**Caso real-alvo**: residência unifamiliar térrea, 80m², estrutura concreto, fundação sapata isolada, sondagem com SPT.

**Entregas**:
- Wizard simples: tipo de obra → planta retangular → pavimentos → CEP → SPT
- Inferência: vento por CEP (NBR 6123), carga acidental NBR 6120
- Motor FEM frame básico (nós + barras 3D, estática linear)
- Dimensionamento NBR 6118: viga (flexão simples), pilar (compressão centrada + flexo-compressão simples)
- Geotecnia: capacidade Terzaghi/Meyerhof + recalque elástico
- Fundação: sapata isolada NBR 6122
- Combinações ELU/ELS NBR 8681
- Relatório PDF com memória de cálculo + citações
- Frontend wizard funcional (sem 3D)

**Não-objetivo**: aço, madeira, lajes complexas, dinâmica, BIM, multi-pavimento alto.

**Sucesso**: usuário leigo cadastra, faz wizard, gera PDF de residência simples em < 15 min, resultado bate com cálculo manual de referência (erro < 1%).

---

## Fase 2 — MVP Completo (estrutura + geotecnia + pro mode) (12 semanas)

**Objetivo**: produto vendável.

**Entregas**:
- Lajes maciças e nervuradas (NBR 6118)
- Aço NBR 8800 (vigas, pilares, treliça)
- Madeira NBR 7190 (residencial)
- Eurocode 2/3 (concreto e aço internacional)
- Geotecnia completa: estaca pré-moldada + hélice contínua + tubulão; correlações Décourt-Quaresma + Aoki-Velloso; perfil estratigráfico multicamada
- Modo Pro: editor paramétrico (input tabular), override de coeficientes
- Importação IFC 4.x (parser)
- Importação CSV/JSON (legacy)
- API REST documentada (OpenAPI)
- Tier free + tier pro com billing (Stripe)
- Dashboard de projetos
- Verificação ELS (flecha, fissuração)
- Lista de materiais (quantitativos)

**Não-objetivo**: ACI 318, sismo, dinâmica modal, alvenaria estrutural, DXF.

**Sucesso**: 50 projetos pagos. NPS > 30. Tempo médio de cálculo PRO < 1h.

---

## Fase 3 — v1.0 GA (20 semanas)

**Objetivo**: produto maduro, escritórios começam a usar.

**Entregas**:
- ACI 318 + AISC 360 (mercado internacional)
- Análise modal + sísmica (NBR 15421, Eurocode 8)
- Análise não-linear física (concreto fissurado)
- Interação solo-estrutura (molas Winkler)
- Recalque por adensamento (Terzaghi 1D)
- Exportação DXF (planta de fôrma e armação)
- Tier Studio (multi-usuário, workspace compartilhado)
- API key + webhooks
- Pen test + relatório SOC 2 light
- Manual técnico completo (web)
- Casos canônicos validados cruzando TQS/SAP2000 (mínimo 30 casos)
- Suporte oficial NBR 6118:2023 (quando publicada)

**Sucesso**: 500 projetos pagos. 5 escritórios usando ativamente. SLA 99.5%. Pen test sem P0/P1.

---

## Fase 4+ — Visão (não comprometida)

- Análise dinâmica avançada (vibração, fadiga)
- Alvenaria estrutural (NBR 16868)
- Plugin Grasshopper (paramétrico nativo)
- Mobile app (read-only + aprovação)
- Marketplace de bibliotecas (perfis customizados, materiais, projetos modelo)
- IA generativa pra pré-dimensionamento (alimentar wizard com modelo treinado em projetos passados)
- Visualização 3D opcional (Three.js, web) — entra **só se** clientes pagantes pedirem em alta frequência
- On-premise (tier Enterprise)
- Multi-region (LATAM + Europa)

---

## Marcos críticos (gates de qualidade)

| Marco | Gate |
|---|---|
| Fim Fase 0 | CI verde + deploy em staging + 1 usuário interno cadastra projeto |
| Fim Fase 1 | 5 casos canônicos NBR 6118 validados com erro < 1% vs livro Carvalho/Filho |
| Fim Fase 2 | 10 escritórios em beta fechado por 4 semanas sem P0 |
| Fim Fase 3 | Pen test sem P0/P1 + 30 casos cruzados com TQS/SAP2000 + SLA 99.5% por 60 dias |

---

## Dependências e riscos

| Risco | Mitigação |
|---|---|
| Validação numérica errada (motor FEM com bug) | Suite de fixtures normativas + bench cruzado obrigatório antes de cada release |
| Concorrente já existe sem detectarmos | Research em background (deep-research wf_027b7cf1) tem que retornar antes de fim Fase 0 |
| Norma muda no meio do caminho | Versionamento de norma desde Sprint 1 |
| Custo de cálculo no servidor (FEM pesado) | Fila Celery + tier com quota; cálculos > 30s só em pro |
| Engajamento baixo do leigo (input wizard ainda confuso) | UX testing em escritório real desde Fase 1 |
| Adoção PRO bloqueada por falta de TQS-import | IFC + CSV via TQS export resolvem 80%; integração nativa só se justificar |
