---
documento: PRE-FLIGHT da planning v1 (calc-3d)
versao: 1
data: 2026-05-31
autor: Olimpo PRE-FLIGHT
projeto: calc-3d → calc-engine
escopo: validar 8 itens do checklist Olimpo antes de liberar Sprint 0
---

# PRE-FLIGHT — Planning v1 (calc-3d)

> Checklist obrigatório (definido em `09-PROCESSO-OLIMPO.md` §B). Esta auditoria roda ANTES de qualquer Sprint 0 ser disparada. Falhou? Bloqueia. Avisa Hera. Aguarda desbloqueio.

---

## Resumo executivo

| # | Item | Veredito |
|---|---|---|
| 1 | Despacho de Hera/Ayla recebido? | ⚠️ |
| 2 | Hermes auditou (varredura inicial)? | ❌ |
| 3 | Atena aprovou arquitetura macro? | ⚠️ |
| 4 | Spec normativa recebida (NBR/EC/ACI claras)? | ✅ |
| 5 | HTML aprovado por Rafael (se UI)? | ⚠️ |
| 6 | Filesystem MCP disponível? | ✅ |
| 7 | Sequential Thinking MCP disponível? | ✅ |
| 8 | Git limpo o suficiente? | ⚠️ |

**3 ✅ · 4 ⚠️ · 1 ❌**

---

## Item 1 — Despacho de Hera/Ayla recebido?

**Veredito: ⚠️ libera com correção**

**Evidência**:
- `docs/planning/00-SUMARIO.md:59-65` cita "Fluxo de aprovação (3 pausas Ayla)" e o papel de Hera como orquestradora.
- `docs/planning/00-SUMARIO.md:69-74` lista War Rooms agendados, sendo `WR-001 — Aprovação desta planning — hoje (após Rafael ler)`.
- `docs/planning/09-PROCESSO-OLIMPO.md:99-104` repete o agendamento de WR-001.
- **NÃO há registro escrito** de Hera ou Ayla autorizando formalmente a redação desta planning. A planning foi escrita; a aprovação está prevista mas pendente. Não existe `docs/dispatches/` nem ata de pré-despacho.
- A própria task `#18 PRE-FLIGHT efetivo da planning` está `in_progress` no momento desta auditoria — o que indica que a planning foi escrita ANTES do PRE-FLIGHT (inversão de ordem).

**Por que falhou (parcial)**: planning v1 já existe (11 arquivos, ~1500 linhas) sem despacho explicitamente registrado. O fluxo correto seria: Rafael pede → Ayla autoriza Hera → Hera dispara Atena/Apolo/Gaia para escrever planning. Aqui o artefato veio antes do despacho documentado.

**Ação concreta**: registrar despacho retroativo em `docs/dispatches/2026-05-31-planning-v1.md` com (a) quem pediu, (b) quando, (c) escopo autorizado. Realizar WR-001 antes de Sprint 0 começar.

**Responsável**: Hera (registra) + Ayla (chancela).

---

## Item 2 — Hermes auditou (varredura inicial)?

**Veredito: ❌ bloqueia**

**Evidência**:
- `docs/planning/00-SUMARIO.md:39-41` lista arquivos a deletar (`cmaker`, `interfaces/foundation_calculator_interface.py`, `interfaces/visualizador_ifc.py`, `main.py`, `simple_calculator.py`, `.DS_Store`) e arquivos a manter (`ifcopenshell` como parser).
- `docs/planning/04-GAPS-E-BUGS.md` (citado em `00-SUMARIO.md:22`) supostamente cataloga B-001..B-011 e arquivos a refatorar.
- `docs/planning/09-PROCESSO-OLIMPO.md:221` define output contract de Hermes: `mapa estrutural → JSON estruturado em docs/scans/`.
- **`docs/scans/` NÃO existe** (verificado via `ls`). Nenhum JSON de varredura Hermes foi produzido.
- `docs/planning/08-SPRINTS.md:15` cita Hermes como agente disponível, mas **nenhuma task de Sprint 0 (S0-T01..T18) é atribuída a Hermes**. A varredura inicial foi pulada.

**Por que falhou**: o output contract de Hermes (JSON em `docs/scans/`) não existe. As decisões de "deletar X, manter Y" em `04-GAPS-E-BUGS.md` foram tomadas sem o artefato formal de varredura — o que viola o PRE-FLIGHT item 2 ("Hermes auditou? Sempre que feature nova" e a planning inteira É feature nova).

**Ação concreta**: Hermes roda varredura completa do repo atual e produz `docs/scans/2026-05-31-baseline-calc-3d.json` com (a) inventário de arquivos, (b) classificação keep/delete/refactor, (c) dependências externas, (d) LoC por módulo. Este artefato vira input do POST-FLIGHT do Sprint 0.

**Responsável**: Hermes (executa varredura) + Hera (despacha).

---

## Item 3 — Atena aprovou arquitetura macro?

**Veredito: ⚠️ libera com correção**

**Evidência**:
- `docs/planning/03-DESIGN.md:295-301` lista 5 ADRs A SEREM DOCUMENTADAS: ADR-001 (FastAPI), ADR-002 (sem 3D), ADR-003 (motor próprio FEM), ADR-004 (multi-tenant via tenant_id), ADR-005 (Postgres).
- `docs/planning/08-SPRINTS.md:46` (S0-T15): "Documentar ADR-001 (FastAPI), ADR-002 (sem 3D), ADR-005 (Postgres) | Atena + Gaia | médio | docs/adr/*.md".
- **`docs/adr/` NÃO existe** (verificado via `ls`). Nenhuma ADR está escrita.
- `docs/planning/08-SPRINTS.md:222`: "Atena | ADRs + arquitetura | input pontual" — papel reduzido.
- A planning afeta MUITO MAIS que 3 módulos (deleta 5+ arquivos, troca stack inteira PyQt6→FastAPI, cria 4 layers core/apps/infra/tests, adiciona Postgres+Redis+Celery, multi-tenant). Isso EXIGE Atena no driver seat.

**Por que falhou (parcial)**: as decisões arquiteturais estão tomadas e documentadas em prosa em `03-DESIGN.md`, mas o output contract de Atena (`docs/architecture/` ou `docs/adr/*.md` em Markdown formal — `09-PROCESSO-OLIMPO.md:223`) não foi entregue. ADR-003 (motor FEM próprio) inclusive ESTÁ EM CONFLITO com WR-002 agendado ("motor FEM: próprio vs opstool/OpenSeesPy" — fim Sprint 1) — ou seja, a decisão está pré-cozida na planning mas vai pra War Room depois. Inconsistência.

**Ação concreta**: Atena escreve formalmente ADR-001..ADR-005 em `docs/adr/` ANTES de Sprint 0 começar. ADR-003 fica marcada `status: provisional` até WR-002. Sem isso, Apolo está autorizado a violar V-FLIGHT no S0-T04 (criar `pyproject.toml`).

**Responsável**: Atena (escreve ADRs) + Hera (cobra).

---

## Item 4 — Spec normativa recebida (NBR/EC/ACI claras)?

**Veredito: ✅ aprovado**

**Evidência**:
- `docs/planning/02-REQUIREMENTS.md:50-58` (RF-5) lista normas estruturais explicitamente: NBR 6118 (concreto), NBR 8800 (aço), NBR 7190 (madeira, v1.5), Eurocode 2 e 3, ACI 318 + AISC 360 (v1.5), NBR 15421 (sísmica, v2).
- `docs/planning/02-REQUIREMENTS.md:60-69` (RF-6) lista normas geotécnicas: NBR 6122 (fundações), Terzaghi/Meyerhof/Vesic/Brinch-Hansen (capacidade), Décourt-Quaresma/Aoki-Velloso (estaca via SPT).
- `docs/planning/02-REQUIREMENTS.md:71-77` (RF-7) lista normas de carga: NBR 6120 (acidental), NBR 6123 (vento), NBR 8681 (combinações).
- `docs/planning/02-REQUIREMENTS.md:91-94` (RF-10) exige versionamento de norma e citação inline ("verificação X conforme NBR 6118:2014, item 17.3.2.2").
- `docs/planning/00-SUMARIO.md:43`: "versionamento de norma desde o dia 1 — NBR 6118:2014, NBR 6122:2022, etc."
- `docs/planning/09-PROCESSO-OLIMPO.md:46-54` adapta o item PRE-FLIGHT 4 corretamente para o domínio: Apolo não implementa cálculo sem citação da norma + fórmula explícita + fixture esperado.

**Conclusão**: as normas estão LISTADAS e PRIORIZADAS (MUST/SHOULD com versão MVP/v1.5/v2). Suficiente como spec macro. Specs detalhadas (item-da-norma + fórmula + fixture) virão sprint a sprint, conforme contrato de Atena em `09-PROCESSO-OLIMPO.md`.

**Sem ação requerida** neste item.

---

## Item 5 — HTML aprovado por Rafael (se UI)?

**Veredito: ⚠️ libera com correção**

**Evidência**:
- `docs/planning/06-FLUXOS-DE-TELA.md` tem 24 telas (T-01 a T-60) em wireframes ASCII (verificado linhas 1-80).
- `docs/planning/00-SUMARIO.md:62`: "Aprovação dos wireframes (após Sprint 1, T-04 + T-10 mockados em HTML real)" — pausa #2 do Rafael.
- `docs/planning/08-SPRINTS.md:72` (S1-T08): "Frontend: Dashboard projetos (T-04), criar projeto vazio | Íris | grande | tela conforme T-04".
- `docs/planning/08-SPRINTS.md:158` (S5-T07): "Frontend: wizard T-10 (5 passos) | Íris | épico | UX teste com 3 usuários".
- **PROBLEMA**: o wizard (T-10) só tem mockup HTML em **Sprint 5** (semanas 11-12). Mas Rafael aprovou que `00-SUMARIO.md:62` mockup HTML aconteça **após Sprint 1**, com T-04 + T-10. O cronograma INTERNO de sprints (`08-SPRINTS.md`) joga T-10 pra Sprint 5, contradizendo a Pausa #2 prometida em `00-SUMARIO.md`.

**Por que falhou (parcial)**: wireframes ASCII existem ✅. Mas HTML interativo aprovado por Rafael não existe e o cronograma está inconsistente: Sumário promete pausa após Sprint 1; sprints colocam T-10 só em Sprint 5. Sprint 5 NÃO TEM task de mockup HTML aprovado por Rafael ANTES de implementação — pula direto pra construção React.

**Ação concreta**:
- Mover criação de mockup HTML estático de T-04 + T-10 (Íris, sem stack, só Tailwind/HTML puro) para **Sprint 1 task adicional S1-T13**.
- Criar gate explícito em Sprint 5 que exige aprovação HTML antes de S5-T07.
- Ou: renegociar com Rafael: pausa #2 acontece após Sprint 1 (T-04 only) e DE NOVO antes de S5-T07 (T-10 wizard).

**Responsável**: Íris (produz HTML) + Ayla (intermedia aprovação Rafael) + Hera (corrige cronograma).

---

## Item 6 — Filesystem MCP disponível?

**Veredito: ✅ aprovado**

**Evidência**:
- Esta sessão executou Read (`/Users/rafaeldias/IdeaProjects/calc-3d/docs/planning/00-SUMARIO.md`, `02-REQUIREMENTS.md`, `08-SPRINTS.md`, `09-PROCESSO-OLIMPO.md`, `06-FLUXOS-DE-TELA.md`, `01-REGRA-DE-NEGOCIO.md`) com sucesso.
- Bash executou `ls`, `git status`, `grep`, `find` com sucesso.
- Write está sendo usado para gerar este próprio arquivo.
- Tools `mcp__filesystem__*` listadas no system-reminder (read_file, list_directory_with_sizes, list_allowed_directories).

**Sem ação requerida**.

---

## Item 7 — Sequential Thinking MCP disponível?

**Veredito: ✅ aprovado**

**Evidência**:
- `mcp__thinking__sequentialthinking` aparece na lista de deferred tools do system-reminder desta sessão.
- Disponível sob demanda via `ToolSearch` (uma chamada para carregar schema antes de invocar).
- Será necessário, por exemplo, em validações numéricas complexas dos sprints S2 (FEM frame 3D), S3 (NBR 6118), S4 (geotecnia) — exatamente os casos previstos no PRE-FLIGHT item 7 ("validação numérica complexa", `09-PROCESSO-OLIMPO.md:41`).

**Sem ação requerida**.

---

## Item 8 — Git limpo o suficiente pra trabalhar?

**Veredito: ⚠️ libera com correção (não bloqueia, mas exige higiene)**

**Evidência** (`git status` em `/Users/rafaeldias/IdeaProjects/calc-3d`):
```
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  new file:   laura-maio26.txt

Untracked files:
  .idea/
  docs/
```

Análise:
- **Branch correta**: `main`, alinhada com `origin/main` (✅ conforme `00-SUMARIO.md:42`).
- **Staged**: `laura-maio26.txt` — arquivo solto na raiz, não pertence à planning. Provavelmente nota da Laura/Ayla. Decidir: commitar separado ou descartar.
- **Untracked `.idea/`**: deve ir pro `.gitignore` (já previsto em S0-T02 — `08-SPRINTS.md:33`).
- **Untracked `docs/`**: a planning inteira (11 arquivos + este PRE-FLIGHT) está untracked. Não é blocker, mas precisa de commit dedicado "feat(docs): planning v1" antes de Sprint 0 começar pra ter ponto de retorno.
- Não bloqueia trabalho — main está clean o suficiente. Mas commitar a planning ANTES de S0-T01 (que vai deletar `cmaker`, `main.py` etc) é essencial pra não misturar diff "doc + delete" no mesmo commit.

**Por que ⚠️ e não ✅**: o estado atual MISTURA três coisas (`laura-maio26.txt` staged, `.idea/` lixo, `docs/` legítimo untracked). Antes de Sprint 0 dar `git rm` em arquivos do legado, o working tree precisa estar limpo e a planning precisa ser commit isolado.

**Ação concreta**:
1. Decidir destino do `laura-maio26.txt` (mover pra `docs/` ou descartar do staging).
2. `git add docs/planning/ && git commit -m "feat(docs): planning v1 + processo Olimpo aplicado"`.
3. Adicionar `.idea/` ao `.gitignore` (S0-T02 antecipado).
4. `git status` deve ficar clean antes de S0-T01 rodar.

**Responsável**: Apolo (executa) + Ayla (decide o `laura-maio26.txt`).

---

## VEREDITO GERAL

# ⚠️ LIBERA COM CORREÇÕES BLOQUEADORAS

A planning v1 é **substantiva e bem estruturada** (✅ normas claras, ✅ MCPs ativos, ✅ git em `main` operável). Mas **viola o próprio processo Olimpo que ela mesma define** em três pontos críticos:

1. **Hermes não auditou** (item 2 = ❌). A planning tomou decisões de "deletar X, manter Y" sem o artefato formal de varredura. Isso é V-FLIGHT no nascedouro do projeto.
2. **Atena não emitiu ADRs** (item 3 = ⚠️). 5 ADRs estão listadas como "a documentar" mas nenhuma existe em `docs/adr/`. A arquitetura está em prosa (`03-DESIGN.md`), não em ADR formal.
3. **Mockup HTML não está no caminho certo** (item 5 = ⚠️). `00-SUMARIO.md` promete pausa Rafael após Sprint 1; `08-SPRINTS.md` joga T-10 pra Sprint 5. Inconsistência interna.

Sprint 0 NÃO PODE começar até as ações abaixo serem executadas.

---

## LISTA DE AÇÕES BLOQUEADORAS

| # | Ação | Responsável | Prazo |
|---|---|---|---|
| A1 | Hermes roda varredura inicial e produz `docs/scans/2026-05-31-baseline-calc-3d.json` | Hermes (despacho Hera) | antes de S0-T01 |
| A2 | Atena escreve ADR-001..ADR-005 em `docs/adr/` (ADR-003 marcada `provisional` até WR-002) | Atena + Gaia | antes de S0-T01 |
| A3 | Hera registra despacho retroativo da planning em `docs/dispatches/2026-05-31-planning-v1.md` | Hera | antes de WR-001 |
| A4 | WR-001 efetivo (ata + voto registrado em `docs/debates/WR-001-aprovacao-planning.md`) | Hera facilita; Atena/Apolo/Íris/Hefesto/Ayla votam | hoje |
| A5 | Decidir destino de `laura-maio26.txt`; commit isolado da planning; adicionar `.idea/` ao `.gitignore` | Apolo executa; Ayla decide arquivo Laura | antes de S0-T01 |
| A6 | Reconciliar inconsistência mockup HTML: criar S1-T13 (mockup T-04 + T-10) OU desdobrar pausa Rafael em duas (após S1 e antes de S5-T07) | Íris propõe; Hera ajusta `08-SPRINTS.md`; Ayla aprova | antes de Sprint 1 |

---

## Não-bloqueadores (mas registrar)

- ADR-003 (motor próprio FEM) está em **conflito direto** com WR-002 (decidir entre próprio vs opstool). Marcar como `provisional` na ADR. Decisão final = ata WR-002 fim Sprint 1.
- Madeira NBR 7190 sobe de SHOULD pra MUST na Fase 2 (`00-SUMARIO.md:45`) — mas em `02-REQUIREMENTS.md:53` está como SHOULD/v1.5. Atualizar `02-REQUIREMENTS.md` ou registrar override em ADR-006.
- Distribuição de carga em Fase 1 (`08-SPRINTS.md:218`): Apolo com ~50 tasks vs Íris com ~12. Validar viabilidade no PARALLELISM CAP de 2 writers (`09-PROCESSO-OLIMPO.md:208-212`) — Apolo pode virar gargalo.

---

**Fim do PRE-FLIGHT.** Próximo passo: Hera lê esta auditoria, despacha A1 + A2 em paralelo (read-only Hermes + write Atena, cap 2 ok), agenda WR-001 com a planning + este PRE-FLIGHT como input.
