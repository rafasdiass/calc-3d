---
projeto: calc-3d (futuro: calc-engine)
status: planning-v1
data: 2026-05-31
branch_base: main
decisao_arquitetural: backend-only · sem GUI desktop · sem viewer 3D
mercado: Brasil + global
escopo: estrutura completa multi-material com fundação multi-solo
camadas_usuario: leigo (input mínimo) + profissional (override paramétrico)
---

# 00 — SUMÁRIO

## Índice da planning

| # | Arquivo | Propósito |
|---|---|---|
| 00 | `00-SUMARIO.md` | este — índice + executivo |
| 01 | `01-REGRA-DE-NEGOCIO.md` | regra de negócio detalhada (visão, missão, problema, solução, escopo, modelo, KPIs, compliance) |
| 02 | `02-REQUIREMENTS.md` | requisitos funcionais (RF) e não-funcionais (RNF) com priorização MUST/SHOULD/MAY |
| 03 | `03-DESIGN.md` | arquitetura técnica, stack, estrutura de pastas, modelos de domínio, fluxos macro, ADRs |
| 04 | `04-GAPS-E-BUGS.md` | arquivos a deletar, refatorar, bugs (B-001..B-011), gaps de domínio, dívida técnica |
| 05 | `05-ROADMAP.md` | 4 fases (Fundação → MVP Concreto → MVP Completo → v1.0 GA) em 12 meses |
| 06 | `06-FLUXOS-DE-TELA.md` | wireframes textuais (T-01 a T-60), princípios UX, estados de erro, critérios aceitação |
| 07 | `07-INFOGRAFICOS.md` | 7 diagramas ASCII: arquitetura, jornada usuário, fluxo NBR 6118, solo→fundação, modelo dados, pipeline release, fases |
| 08 | `08-SPRINTS.md` | 23 sprints de 2 semanas, ~120 tasks atribuídas (Apolo, Íris, Hefesto, Artemis, Atena, Gaia) |
| 09 | `09-PROCESSO-OLIMPO.md` | governança: PRE-FLIGHT, POST-FLIGHT, WAR ROOM, HANDOFF, ESCALATION 5 tiers, output contracts |
| 10 | `10-RESEARCH-COMPETITIVO.md` | benchmark adversarial: 9 concorrentes, gap, stack referência, pricing, 21 fontes verificadas |
| 11 | `11-FRONTEND.md` | planning frontend formalizado (stack, telas, componentes) |
| ADR | `docs/adr/0001..0007` | decisoes arquiteturais formais |
| Scan | `docs/scans/2026-05-31-baseline-calc-3d.json` | varredura Hermes inicial |
| WR | `docs/debates/WR-001-aprovacao-planning.md` | ata da aprovacao |
| Dispatch | `docs/dispatches/2026-05-31-planning-v1.md` | despacho retroativo |
| PRE-FLIGHT | `docs/planning/PRE-FLIGHT-PLANNING-V1.md` | checklist 8 itens executado |

## Executivo (5 linhas)

calc-3d é hoje uma calculadora desktop PyQt6 com 11 fundações e viewer IFC. Vamos descartar GUI/3D, manter ~1.500 linhas de motor de cálculo (calculators puros, sem dep de GUI) e construir um **backend SaaS de cálculo estrutural multi-material com fundação multi-solo**. O diferencial é a **camada simples** (input mínimo → resultado normativo confiável) com **fallback pro modo paramétrico profissional**. Concorrentes diretos: TQS, Eberick, CYPE (BR) + SkyCiv, SAP2000, RFEM (global). Ângulo de entrada **(verificado pelo research)**: SaaS web nativo + NBR-first + input mínimo (motor automático) + foundation multi-solo embutido — combinação que **nenhum concorrente atual oferece**.

## Decisões já tomadas

1. **sem 3D no MVP** — render não é diferencial, é custo. Esquemas 2D + tabelas + relatório PDF resolvem.
2. **sem GUI desktop** — tudo via API HTTP. Front separado (React + Vite + TS), web responsivo.
3. **stack Python 3.12 + FastAPI** — aproveita 100% dos calculators existentes em Python puro.
4. **deletar**: `cmaker`, `interfaces/foundation_calculator_interface.py`, `interfaces/visualizador_ifc.py`, `main.py`, `simple_calculator.py`, todos os `.DS_Store`. Adicionar ao `.gitignore`.
5. **manter como parser**: `ifcopenshell` (sem `.geom`) pra ler metadados IFC (modo PRO).
6. **branch operacional**: `main`. `installer` é descartável (só `cmaker` + `.DS_Store`). Já voltei pra `main`.
7. **renomear projeto**: `lct_calculator` → `calc_engine`.
8. **versionamento de norma desde o dia 1** — NBR 6118:2014, NBR 6122:2022, etc.
9. **avaliar opstool/OpenSeesPy** como motor FEM (research aponta como melhor caminho que motor próprio do zero) — decisão final em War Room WR-002 (fim Sprint 1).
10. **madeira NBR 7190 sobe de SHOULD pra MUST na Fase 2** — research mostrou que Eberick não tem madeira, virando diferencial real.
11. **processo Olimpo aplicado** — PRE-FLIGHT, POST-FLIGHT, ESCALATION 5 tiers, HANDOFF com evidência runtime obrigatória, War Rooms agendados (WR-001, WR-002, WR-003, WR-004).
12. WR-002 (motor FEM) antecipado pra fim Sprint 0
13. Bench cruzado nao usa TQS/Eberick — referencia primaria: Carvalho/Filho (concreto), Velloso/Lopes (geotecnia)
14. `laura-maio26.txt` movido pra `docs/private/` + adicionado ao .gitignore
15. API versionada `/api/v1/...` desde Sprint 0
16. OpenAPI codegen TS gera `@calc-engine/api-types` no CI (sem drift FE/BE)

## O que o research validou (workflow wf_027b7cf1-111 — 23 claims confirmadas, 2 refutadas)

✅ Nenhum concorrente combina SaaS web + NBR + multi-material + multi-solo + API moderna. **Gap real.**
✅ SkyCiv prova que SaaS estrutural cloud com multi-solo é viável tecnicamente — mas não tem NBR.
✅ Eberick não lista madeira na página oficial — diferencial brasileiro.
✅ RFEM, SAP2000, ETABS, Tekla SD são desktop premium (cloud só auxiliar).
✅ Pricing competitivo: faixa R$ 100-300/mês (Pro autônomo) é ordem de grandeza abaixo de Eberick.
✅ opstool (Python wrapper OpenSeesPy, peer-reviewed SoftwareX 2025) entrega "input mínimo + precisão automática" via fiber meshing automático, conversão de unidades, lumped mass, step-size adjustment.

❌ Refutado: arquitetura de interação solo-estrutura via interface elements como obrigatória — vamos com molas Winkler (mais simples, mais comum em projetos cotidianos).

## Fluxo de aprovação (3 pausas Ayla)

1. **Aprovação da planning** (esta pausa) — Rafael lê, ajusta, aprova ou rejeita.
2. **Aprovação dos wireframes** (após Sprint 1, T-04 + T-10 mockados em HTML real)
3. **Entrega final v0.1.0-beta** (fim Sprint 6, Rafael abre PR no GitHub)

Fora dessas 3 pausas: Hera orquestra, Apolo/Íris implementam, Hefesto valida, Artemis revisa, Ayla aprova handoff. Rafael só recebe entrega ou aviso de incidente.

## War Rooms agendados

| ID | Tema | Quando |
|---|---|---|
| WR-001 | Aprovação desta planning | hoje (após Rafael ler) |
| WR-002 | Motor FEM: próprio vs opstool/OpenSeesPy | fim Sprint 1 |
| WR-003 | Pricing final (após validar TAM) | fim Sprint 4 |
| WR-004 | ACI 318 antes da Fase 3? | fim Sprint 9 |

## Próximo passo (após aprovação)

1. Hera dispara Sprint 0 com S0-T01 (deletar arquivos descartáveis) → S0-T18 (review)
2. Em paralelo, atualizações nos arquivos da planning forçadas pelo research (`10-RESEARCH-COMPETITIVO.md` seção J)
3. Fim Sprint 0: gate "hello world" rodando + CI verde + signup/login funcional
