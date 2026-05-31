---
documento: processo Olimpo aplicado ao calc-3d
versao: 1.0
data: 2026-05-31
fonte: inventory/source-maps/bcm-ayla/operational/ (PRE_FLIGHT, POST_FLIGHT, DISPATCH, ESCALATION, HANDOFF, OUTPUT_CONTRACTS)
escopo: governança operacional do projeto
---

# 09 — PROCESSO OLIMPO (PRE-FLIGHT, WAR ROOM, HANDOFF, ESCALATION)

> Este documento adapta o protocolo operacional do Olimpo (definido em `inventory/source-maps/bcm-ayla/operational/`) ao projeto calc-3d. Algumas regras existem no Olimpo para o domínio clínico (ABA/BCM) — aqui adaptadas para o domínio de **engenharia estrutural normativa**.

---

## A. Princípio fundamental

```
Rafael fala com Ayla. Ayla fala com Rafael.
Hera orquestra. Agentes implementam. Hefesto valida. Artemis revisa.
Rafael só vê: pausa de planning · pausa de mockup · entrega final.
```

Tudo o resto é interno ao Olimpo.

---

## B. PRE-FLIGHT (checklist universal antes de agir)

Todo agente verifica antes de qualquer ação de implementação. Falhou? **BLOQUEADO** → informa Hera → aguarda desbloqueio.

### Checklist obrigatório

| # | Item | Quando aplica |
|---|---|---|
| 1 | Despacho de Hera recebido? | Sempre (exceto Hermes em varredura inicial) |
| 2 | Hermes auditou? | Feature nova |
| 3 | Atena aprovou arquitetura? | Mudança em 3+ módulos |
| 4 | **Spec normativa recebida?** ⬅ adaptado | Código de cálculo estrutural ou geotécnico |
| 5 | HTML aprovado por Rafael? | Componente visual com UI nova |
| 6 | Filesystem MCP disponível? | Sempre |
| 7 | Sequential Thinking MCP disponível? | Validação numérica complexa |
| 8 | Git limpo? | Antes de commitar |

### Adaptação domain-specific (calc-3d)

No Olimpo original o item 4 era "Afrodite spec recebida (clínico)". Aqui vira:

> **"Spec normativa recebida"** — Apolo não implementa cálculo NBR/Eurocode/ACI sem que Atena (arquitetura) tenha entregue:
> - Citação do item da norma (ex: NBR 6118:2014 §17.2.2)
> - Fórmula explícita (ex: `As = Md / (z·fyd)`)
> - Fixture esperado (input de teste + output de referência de livro/manual)
>
> Implementar cálculo "de cabeça" sem essa spec = **V-NORM**, registrado em retro.

---

## C. POST-FLIGHT (checklist após implementação)

Todo agente implementador verifica antes de entregar handoff.

| # | Item | Critério |
|---|---|---|
| 1 | Arquivos realmente modificados? | `git diff --name-only` confirma |
| 2 | Build compila? | `python -m build` ou `pytest --collect-only` sem erro |
| 3 | Testes passam? | `pytest path/to/test.py -v` output colado |
| 4 | Lint limpo? | `ruff check` + `mypy` sem erro |
| 5 | Servidor inicia? | `uvicorn apps.api.main:app` responde 200 em /health |
| 6 | Funcionalidade funciona? | curl ou HTTP client retorna esperado |
| 7 | **Validação numérica?** ⬅ específico calc-3d | Fixture de norma roda, erro < 1% vs valor esperado |

**Handoff sem evidência runtime = Hera REJEITA automaticamente.**

---

## D. WAR ROOM (decisões macro com múltiplos agentes)

War Room é convocado quando:
- decisão arquitetural afeta 3+ módulos
- há impasse entre 2+ agentes que ESCALATION Tier 1-4 não resolveu
- risco de regressão sistêmica
- escolha de stack/tooling crítico

### Estrutura de War Room calc-3d

```
👑 HERA (facilitador)
🛡️ ATENA (arquitetura) — voto técnico
🔥 APOLO (BE) — voto técnico backend
🌈 ÍRIS (FE) — voto técnico frontend
🏹 ARTEMIS (TL) — voto integração
🔨 HEFESTO (QA) — voto qualidade
👸 AYLA (PO) — voto produto (irrevogável em escopo)
```

**Não há Afrodite no calc-3d.** O domínio é normativo, não clínico. O equivalente em peso é a **veracidade normativa**: se uma decisão viola NBR/EC/ACI, é Atena quem veta com citação da norma, e o veto é irrevogável (mesmo nível de Afrodite no original).

### War Rooms já agendados

| ID | Tema | Quando | Participantes |
|---|---|---|---|
| WR-001 | Aprovação desta planning | hoje (após Rafael ler) | Hera, Atena, Apolo, Íris, Hefesto, Ayla |
| WR-002 | Escolha do motor FEM (próprio vs OpenSees via opstool) | fim Sprint 1 | Atena, Apolo, Hefesto |
| WR-003 | Tier de pricing (após research validar TAM) | fim Sprint 4 | Ayla, Atena |
| WR-004 | Ir ou não pra ACI 318 antes da Fase 3 | fim Sprint 9 | Ayla, Atena, Apolo |

Cada War Room gera artifact em `docs/debates/WR-NNN-tema.md` com voto registrado.

---

## E. HANDOFF (formato obrigatório)

Todo agente entrega assim:

```
[EMOJI] [NOME] — [fase]

[Resumo: 1-3 linhas]

EVIDÊNCIA:
- Arquivos modificados: [lista com paths reais]
- Build: [output colado ou "N/A"]
- Testes: [output colado ou "N/A"]
- Runtime: [output ou "N/A"]
- Validação numérica: [fixture comparada com valor esperado, % de erro]

[Artefato em arquivo separado, se houver]

→ [Próximo agente]: [ação específica]
```

### Exemplo CORRETO (calc-3d)

```
🔥 APOLO — backend NBR 6118 viga implementada

Método dimensionar_viga_flexao_simples() implementado em
core/design/concrete/nbr6118.py com domínios 2, 3 e cálculo de As mín.

EVIDÊNCIA:
- Arquivos: core/design/concrete/nbr6118.py (linhas 84-220), tests/unit/test_nbr6118_beam.py
- Build:
  $ python -m build
  Successfully built calc_engine-0.1.0
- Testes:
  $ pytest tests/unit/test_nbr6118_beam.py -v
  ✓ test_dominio_2_armadura_simples PASSED
  ✓ test_dominio_3_armadura_simples PASSED
  ✓ test_armadura_minima_rho_min PASSED
  ✓ test_carvalho_filho_exemplo_4_1 PASSED (erro 0.3% vs livro)
  4 passed in 0.42s
- Validação numérica: exemplo Carvalho/Filho 4.1 — As esperado 4.12 cm², calculado 4.13 cm² (erro 0.24%)

→ Hefesto: roda suite completa de fixtures NBR + benchmark cruzado vs TQS (caso T-001)
```

### Exemplo REJEITADO

```
🔥 APOLO — implementei NBR 6118 viga

Build ok, testes passando.

→ Artemis: integra.
```

**Hera REJEITA: "build ok" não é evidência. Cole o output. Cole o erro relativo da fixture.**

---

## F. ESCALATION (5 tiers — Rafael é último recurso)

| Tier | Quem decide | Tipo de decisão |
|---|---|---|
| 1 | **Ayla** | técnica/padrão (path, naming, fix strategy, refactor escopo) |
| 2 | **Atena** | arquitetural macro (3+ módulos, schema irreversível, migration) |
| 3 | **Atena (com citação de norma)** ⬅ adaptado | normativa (qual norma aplicar, qual coeficiente, qual método) |
| 4 | **Hera** | conflito multi-agente (Apolo vs Íris, Apolo vs Atena, etc.) |
| 5 | **Rafael** | produto/negócio sem precedente OU impasse Tier 1-4 esgotado |

### Adaptação domain-specific

No Olimpo original Tier 3 era "Afrodite (clínico)". Aqui vira:

> **Atena com citação de norma é veto irrevogável.** Se Apolo quiser implementar ACI 318 e o projeto está marcado como "NBR 6118 obrigatória", Atena veta citando a regra de negócio (`01-REGRA-DE-NEGOCIO.md` e o standards.config do projeto). Apolo não pode contornar — só Ayla pode mudar a regra.

### Violação de escalação

Apolo escala direto pro Rafael ("rafa, qual norma?") sem passar por Ayla → **V-ESCALATION**, registrada em retro.

### Não escala pra Rafael

❌ Bug de código (Hefesto bloqueia → Apolo corrige)
❌ Override de coeficiente normativo discutível (Atena cita norma → decisão)
❌ Conflito Apolo vs Íris sobre contrato DTO (Hera medeia)
❌ Performance ruim (Hefesto sinaliza → Apolo otimiza)

✅ Escala pra Rafael APENAS:
- Planning aprovada (PAUSA 1)
- Mockup aprovado (PAUSA 2)
- Feature completa pra PR (PAUSA 3)
- Impasse Tier 1-4 esgotado em > 1h (exceção)

---

## G. PARALLELISM CAP

Hardware-aware. Para o ambiente local (M4/16GB) o cap é:

- **Sprint com Apolo/Íris/Artemis (writers)**: max 2 em paralelo
- **Sprint só read-only (Hermes/Atena/Hefesto-audit/Gaia)**: max 4 em paralelo
- **Sprint mista**: usa o menor cap = 2

Hera respeita isso ao despachar.

---

## H. OUTPUT CONTRACTS (formato esperado por agente)

| Agente | Saída | Formato |
|---|---|---|
| Hermes | mapa estrutural | JSON estruturado em `docs/scans/` |
| Atena | arquitetura | Markdown + diagrama em `docs/architecture/` ou `docs/adr/` |
| Apolo | código + testes | diff + output pytest |
| Íris | mockup OU componente | HTML interativo OU diff React + screenshot |
| Artemis | integração | diff facade + output curl/HTTP |
| Hefesto | QA report | Markdown checklist + coverage |
| Gaia | docs | Markdown publicado (ou Notion via MCP) |
| Ayla | aprovação/rejeição | mensagem curta com voz Laura |

---

## I. VIOLAÇÕES (registradas em audit log)

| Código | O que é | Penalidade |
|---|---|---|
| V-NORM | Implementar cálculo sem spec normativa de Atena | Hera bloqueia merge, Apolo refaz |
| V-ESCALATION | Agente escala direto pro Rafael sem passar Tier 1-4 | Registrado em retro |
| V-EVIDENCE | Handoff sem output runtime colado | Hera rejeita automaticamente |
| V-FLIGHT | Agente age sem PRE-FLIGHT confirmado | Bloqueio automático no CI (hook) |
| V-SCOPE | Mudança fora do escopo do sprint atual | Ayla decide: aceita como INC ou rejeita |

Log: `~/.claude/ayla-violation-audit.log`

---

## J. RITMO E CADÊNCIA

- **Daily** (assíncrono): Hera atualiza `docs/status/YYYY-MM-DD.md` com tasks completadas + bloqueios + próximas
- **Sprint review** (a cada 2 semanas): Hera + Ayla consolidam, atualizam `08-SPRINTS.md`, abrem War Room se houver bloqueio sistêmico
- **Pausa Rafael**: 3x por release (planning, mockup, entrega final)
- **Retro** (fim de fase): registrar decisões, violações, lições — em `docs/retros/fase-N.md`

---

## K. INTEGRAÇÃO COM A PLANNING

Este documento **é parte do contrato** desta planning. Aprovar a planning = aprovar o processo Olimpo aplicado a este projeto.

Se Rafael quiser ajustar (ex: "quero ver toda decisão de norma, não confio no Atena sozinha") — atualizar este arquivo antes da Sprint 0.
