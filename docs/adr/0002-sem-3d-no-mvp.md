---
adr: 0002
title: Sem visualizacao 3D no MVP
status: accepted
date: 2026-05-31
deciders: [Atena, Ayla]
consulted: [Apolo, Hefesto]
informed: [Iris, Artemis, Hera]
---

# ADR-0002 — Sem visualizacao 3D no MVP

## Contexto

O calc-3d nasceu com nome carregando o "3D" e o desktop PyQt6 originalmente cogitou viewer 3D para estruturas. Na transicao para SaaS, a pergunta volta: o MVP precisa de viewer 3D web (Three.js/Babylon.js) ou desktop 3D (Qt3D, VTK)?

A analise de mercado (planning/02) mostra que o concorrente cloud mais relevante, SkyCiv, oferece 3D leve mas o valor central vendido nao e a renderizacao — e a precisao do calculo, a cobertura de normas e a velocidade de entrega de relatorio. TQS, Eberick e Cypecad possuem 3D pesado mas sao desktop e o 3D la e suporte a modelagem, nao diferenciador comercial.

O publico do MVP (calculista PJ, escritorio pequeno, engenheiro junior) precisa de: entrar dados, validar, calcular, sair com PDF assinavel e DXF para projetista. Renderizacao 3D web bem feita custa: dependencia pesada (Three.js + react-three-fiber + drei), sincronizacao de estado de cena com modelo de dominio, performance em mobile, complexidade de testes E2E, custo de UX para construir (camera, picking, gizmos).

A janela de tempo do MVP (Sprint 0 a 4) nao comporta entregar 3D bom. 3D ruim e pior que sem 3D — passa amadorismo.

## Opcoes consideradas

1. **Viewer 3D web (Three.js + react-three-fiber)** — Pros: visualmente impressionante, paridade com SkyCiv. Cons: 3-4 semanas de engenharia front + back para sincronia; bundle pesado; risco de UX quebrada; nao move ponteiro de receita no MVP.
2. **Viewer 3D desktop (Qt3D ou VTK)** — Pros: ja existia no PyQt6 como direcao. Cons: o produto agora e SaaS web, viewer desktop e off-strategy; descartado por incompatibilidade arquitetural.
3. **Sem 3D, esquemas 2D + tabelas + PDF** — Pros: foco no valor real (calculo correto, relatorio assinavel), entrega rapida, manutencao baixa, validacao de mercado antes de investir em viewer. Cons: percepcao de "produto basico" em demos; perda de wow-factor; alguns leads podem comparar mal com TQS.

## Decisao

Adotamos **sem viewer 3D no MVP**. A entrega visual sera composta por:
- Esquemas 2D (planta, corte, vista) gerados via SVG/canvas no front e replicados no PDF.
- Tabelas de resultados (esforcos, deslocamentos, taxas de armadura, verificacoes por norma).
- Diagramas de momento/cortante 2D por barra.
- Exportacao DXF para o projetista abrir em CAD.

Viewer 3D web (Three.js) volta como item da v2 do tier Pro, contingente a validacao de pelo menos 50 clientes pagantes pedindo explicitamente. SkyCiv valida que cloud sem 3D pesado funciona comercialmente.

## Consequencias

- **Positivas**: reduz escopo MVP em ~3 semanas; foco em precisao numerica e cobertura de normas (diferencial real); bundle front leve (mobile-friendly); manutencao baixa; testes E2E mais simples.
- **Negativas**: demos perdem impacto visual contra concorrentes 3D; alguns leads vao filtrar negativamente sem entender o produto; precisamos compensar com case-study e screenshots de relatorio.
- **Riscos**: percepcao de "produto inferior" em fase de aquisicao (mitigado: posicionamento claro de "calculista, nao maquete"; landing page mostra PDF e tabelas, nao 3D). Caso pesquisa pos-MVP mostre que 3D e bloqueador real de venda, abrir ADR-NNNN para reavaliar prioridade da v2.

## Referencias

- /Users/rafaeldias/IdeaProjects/calc-3d/docs/planning/03-DESIGN.md (Front — "Sem Three.js no MVP")
- /Users/rafaeldias/IdeaProjects/calc-3d/docs/planning/02-* (analise competitiva, SkyCiv como prova de mercado)
