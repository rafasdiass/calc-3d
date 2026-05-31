# WR-001 — Aprovacao da Planning v1 (calc-3d -> calc-engine)

**Tipo:** Ata de War Room
**ID:** WR-001
**Data:** 2026-05-31
**Facilitador:** Hera
**PO:** Ayla
**Status final:** APROVADA com correcoes (5/5 APPROVE_WITH_CHANGES, 0 BLOCK)

---

## 1. Tema

Aprovacao da **planning v1** do projeto **calc-3d** (rebatizado simbolicamente como **calc-engine** durante o WR), composta pelos 11 arquivos em `docs/planning/` (00-SUMARIO ate 10-INTEGRACOES, com 11-FRONTEND criado como correcao P0 ainda neste mesmo dia).

Objetivo: validar adversarialmente a planning antes de liberar Sprint 0.

## 2. Participantes

- **Facilitacao:** Hera
- **Votantes (leitura previa obrigatoria dos 11 arquivos):**
  - Atena (arquitetura)
  - Apolo (estimativas / roadmap)
  - Iris (front-end / UX)
  - Hefesto (QA / hardening)
  - Artemis (integracao / contratos)
- **PO consolidador:** Ayla
- **Decisor humano final:** Rafael

## 3. Resultado da votacao

**Placar:** 5 APPROVE_WITH_CHANGES / 0 APPROVE / 0 BLOCK / 0 ABSTAIN

| Agente   | Voto                    | Top 3 concerns                                                                                                                                                  |
|----------|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Atena    | APPROVE_WITH_CHANGES    | 1) ADR-003 conflita com WR-002. 2) RF-5.4 madeira inconsistente entre 03-RF e 05-ARQUITETURA. 3) Falta tipo `NormativeViolation` no modelo de dominio.          |
| Apolo    | APPROVE_WITH_CHANGES    | 1) Sprints 2/3/5 otimistas demais. 2) Antecipar WR-002 para P0 (decisao normativa critica). 3) Bench TQS sem licenca confirmada — risco metodologico.            |
| Iris     | APPROVE_WITH_CHANGES    | 1) Arquivo 11-FRONTEND ausente. 2) Wireframes faltando 8 telas-chave. 3) RNFs de front-end zerados (a11y, perf, i18n nao especificados).                        |
| Hefesto  | APPROVE_WITH_CHANGES    | 1) Cobertura sem `fail-under` configurado. 2) SLO definido sem instrumentacao prevista para Sprint 0. 3) ZAP so na Sprint 6 e `audit_log` sem `REVOKE`.         |
| Artemis  | APPROVE_WITH_CHANGES    | 1) Sem versionamento `/api/v1`. 2) Sem OpenAPI codegen para TS. 3) Sem integration day previsto e sem feature flags na esteira.                                  |

## 4. Decisoes Ayla (consolidacao PO)

Apos consolidar os 15 concerns (3 por votante), Ayla aplicou as seguintes decisoes — algumas escaladas a Rafael:

1. **WR-002 antecipado para o final da Sprint 0** (decisao de Rafael).
   - Motivo: concern critico de Apolo + dependencia de Atena (ADR-003).
2. **Bench cruzado redefinido** (decisao de Rafael):
   - TQS e Eberick **fora** do bench (sem licenca confirmada — concern Apolo procede).
   - Livro **Carvalho/Filho** + **Velloso/Lopes** vira referencia primaria de validacao normativa.
3. **17 correcoes P0/P1 aplicadas em batch hoje** (2026-05-31), cobrindo os 15 concerns + 2 itens cruzados detectados na consolidacao.
4. **`11-FRONTEND.md`** ja criado em paralelo a este WR (resolve concern P0 de Iris).
5. **`laura-maio26.txt`** movido para `docs/private/` (higiene de repositorio detectada durante a varredura).

## 5. Acoes pendentes para liberar Sprint 0

- [ ] Concluir as 17 correcoes P0/P1 em batch (em andamento).
- [ ] Atena entregar ADRs (incluindo ADR-003 alinhado a WR-002).
- [ ] Hermes executar scan formal pos-correcoes.
- [ ] WR-002 agendado para o fim da Sprint 0.

## 6. Proxima pausa para Rafael

- **Evento:** aprovacao do **mockup HTML** (telas T-04 + T-10 estatico).
- **Quando:** fim da **Sprint 1**, conforme cronograma em `00-SUMARIO`.
- **Responsaveis pela entrega:** Iris (mockup) + Gaia (empacotamento dos artefatos).

---

**Referencias cruzadas:**
- Despacho retroativo: `docs/dispatches/2026-05-31-planning-v1.md`
- Planning v1: `docs/planning/00-SUMARIO.md` ... `docs/planning/11-FRONTEND.md`
- Audit log da V-FLIGHT: `~/.claude/ayla-violation-audit.log`
- Workflow de research competitivo: `wf_027b7cf1-111`
