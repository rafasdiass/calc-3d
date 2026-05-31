---
adr: 0003
title: Motor FEM — escolha entre proprio, OpenSeesPy ou Pynite
status: provisional
date: 2026-05-31
deciders: [Atena, Ayla]
consulted: [Apolo, Hefesto]
informed: [Iris, Artemis, Hera]
---

# ADR-0003 — Motor FEM (PROVISIONAL)

## Contexto

O coracao tecnico do calc-3d e o motor de elementos finitos para porticos 3D (vigas/pilares Euler-Bernoulli, opcionalmente Timoshenko com cisalhamento) e, mais adiante, lajes (FEM shell). O motor precisa: montar matriz de rigidez global, aplicar contornos, resolver sistema linear, calcular esforcos por elemento, suportar combinacoes de carga e dialogar com a camada de design por norma (NBR 6118, Eurocode 2/3, AISC 360, NBR 8800).

A decisao tem impacto profundo: troca de motor a posteriori e custosa porque a interface entre core/fem e core/design/* e densa (esforcos por secao critica, envelopes, combinacoes). A escolha precoce errada gera divida tecnica grave; a escolha tardia atrasa o cronograma.

A decisao ainda nao esta cravada porque o Sprint 0 inclui WR-002 — bench cruzado entre as opcoes contra casos canonicos (portico 2D simples, viga continua, pilar engastado-livre) comparando com TQS/SAP2000. Sem o numero do bench, qualquer escolha agora e crenca, nao engenharia.

## Opcoes consideradas

1. **Motor proprio do zero** (numpy + scipy.sparse) — Pros: controle total, footprint minimo, sem dependencia externa que possa quebrar com upgrade Python, customizacao por norma trivial (ex: rigidez fissurada NBR 6118), melhor performance em casos pequenos sem overhead de framework, transparencia total para auditoria/validacao. Cons: precisa implementar, validar e manter; custo inicial alto (montagem, solver, pos-processamento, nao-linearidade futura); risco de bugs sutis em casos edge; sem comunidade para revisao.
2. **opstool / OpenSeesPy** (wrapper Python sobre OpenSees C++) — Pros: motor de pesquisa academica, validado em milhares de papers, suporta nao-linear fisica e geometrica desde o dia 1, materiais avancados (concreto fissurado, plasticidade), ideal se precisarmos de pushover/dinamica; opstool agiliza pre/pos. Cons: dependencia binaria pesada (~50MB), curva de aprendizado da API TCL-style, overhead de chamadas para problemas pequenos, harder to debug, footprint Docker incomodo, customizacao por norma exige envelopar resultados.
3. **Pynite** (FEM frame puro Python, MIT) — Pros: leve, MIT, codigo legivel, comunidade ativa, suficiente para portico 3D linear, integracao trivial com nosso stack, validacao razoavel contra exemplos classicos. Cons: nao-linear limitado, shell em estado experimental, performance inferior a OpenSees em problemas grandes, ainda em evolucao (breaking changes possiveis).

## Decisao

**Decisao adiada para fim do Sprint 0**, registrada na ata WR-002. Status deste ADR permanece **provisional** ate la.

Criterios de decisao no WR-002:
- **Precisao**: erro relativo <1% contra TQS/SAP2000 em 5 casos canonicos.
- **Performance**: portico de 1000 nos / 2000 elementos resolve em <3s (cold) e <1s (warm).
- **Footprint**: imagem Docker final <500MB.
- **Manutenibilidade**: contagem de LoC do adapter + custo estimado de evolucao para shell.
- **Risco**: dependencia externa madura vs codigo proprio com cobertura de testes.

Apos WR-002, este ADR sera atualizado para `status: accepted` com a opcao escolhida, justificativa completa e numeros do bench. Se a escolha for hibrida (ex: Pynite para frame, OpenSeesPy para nao-linear futuro), tambem ficara documentado.

## Consequencias

- **Positivas**: evita compromisso prematuro; bench gera evidencia objetiva; Sprint 0 entrega numero antes de codigo de producao.
- **Negativas**: cronograma do core/fem so destrava apos WR-002; equipe trabalha em mocks da interface no intervalo; risco de retrabalho se bench atrasar.
- **Riscos**: 
  - Bench inconclusivo (mitigado: criterio de desempate = manutenibilidade + footprint).
  - Pynite com bug em caso real apos MVP (mitigado: suite de regressao com casos canonicos rodando em CI).
  - OpenSeesPy quebrar em upgrade Python (mitigado: pin de versao + Docker base estavel).
  - Motor proprio com bug numerico sutil (mitigado: cross-check obrigatorio com pelo menos uma referencia externa em todo release).

## Referencias

- /Users/rafaeldias/IdeaProjects/calc-3d/docs/planning/03-DESIGN.md (Motor de calculo — FEM frame)
- WR-002 — ata de decisao do bench FEM (a produzir no Sprint 0)
- /Users/rafaeldias/IdeaProjects/calc-3d/tests/benchmarks/ (casos canonicos de comparacao)
