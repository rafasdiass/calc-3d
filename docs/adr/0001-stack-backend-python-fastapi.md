---
adr: 0001
title: Stack backend Python 3.12 + FastAPI
status: accepted
date: 2026-05-31
deciders: [Atena, Ayla]
consulted: [Apolo, Hefesto]
informed: [Iris, Artemis, Hera]
---

# ADR-0001 — Stack backend Python 3.12 + FastAPI

## Contexto

O calc-3d ja existe como aplicacao desktop PyQt6, com aproximadamente 1500 LoC em Python implementando calculadoras de fundacoes (sapatas, estacas, tubuloes, blocos, radier), modelos de dominio e geracao de relatorios. A migracao para SaaS exige escolher uma stack backend que sustente API REST multi-tenant, calculos sincronos curtos e fila assincrona para calculos pesados, geracao de PDF/DXF e integracao com motor FEM cientifico (numpy/scipy).

A questao central e: reaproveitar o investimento Python existente, ou reescrever em uma stack que poderia oferecer ganhos de performance ou ergonomia operacional? As alternativas serias sao Flask (Python sincrono classico), Django (Python full-stack monolitico), .NET 8 (C# com performance forte) e Rust + Axum (performance maxima e seguranca de tipos).

Restricoes praticas: equipe de fundacao Python, prazo MVP curto (Sprint 0 a 4), motor de calculo dependente de scipy.linalg/numpy.linalg que nao tem equivalente direto em Rust ou .NET sem custo alto de portabilidade. O MVP precisa entregar valor antes de otimizar runtime.

## Opcoes consideradas

1. **FastAPI 0.110+ sobre Python 3.12** — Pros: aproveita 100% das ~1500 LoC ja escritas, async nativo via Starlette/asyncio, OpenAPI gerado automaticamente, validacao Pydantic v2 (validacao em Rust internamente), ecossistema cientifico (numpy/scipy) sem ponte. Cons: GIL limita paralelismo CPU-bound em processo unico (mitigado por Celery workers), tipagem em runtime mais fraca que linguagens compiladas.
2. **Flask 3 + extensoes** — Pros: mais maduro, footprint menor. Cons: sem async first-class robusto, sem Pydantic/OpenAPI nativos, exigiria empilhar flask-pydantic, flask-smorest, flask-async — reinventando o que FastAPI ja resolve.
3. **Django 5 + DRF** — Pros: bateria inclusa (admin, ORM, auth). Cons: ORM proprio incompativel com SQLAlchemy 2.0 escolhido no design, monolitico demais para arquitetura de microsservicos planejada (api / worker), DRF gera OpenAPI mas com mais ceremonia.
4. **.NET 8 + ASP.NET Core** — Pros: performance superior, tipagem estatica forte, ecossistema empresarial. Cons: portar 1500 LoC de Python (numpy, scipy, calculadoras) e custo proibitivo no MVP, equipe perde meses na transicao, ecossistema cientifico .NET (Math.NET) e mais pobre que SciPy para FEM.
5. **Rust + Axum** — Pros: performance maxima, sem GIL, seguranca de memoria. Cons: Python existente vira lixo, sem biblioteca FEM madura, curva de aprendizado, prazo MVP inviavel. Pode ser usado pontualmente em hot paths do core/fem na v2 via PyO3 se houver gargalo medido.

## Decisao

Adotamos **FastAPI 0.110+ sobre Python 3.12** como stack backend padrao do calc-3d cloud. A escolha preserva o codigo Python existente, alinha-se ao ecossistema cientifico (numpy, scipy, ifcopenshell, ezdxf) que o motor de calculo precisa, e entrega async + OpenAPI + Pydantic v2 sem custo de integracao.

Performance CPU-bound sera tratada via Celery + Redis para calculos longos (>10s), conforme a arquitetura macro do design. Caso surja gargalo medido em hot path numerico, abriremos ADR de extensao em Rust via PyO3 — nao por antecipacao.

## Consequencias

- **Positivas**: reuso imediato de calculators atuais; OpenAPI sem boilerplate; Pydantic v2 valida entrada/saida com performance proxima a Go; equipe produtiva desde dia 1; ecossistema FEM disponivel (Pynite, OpenSeesPy, opstool) sem ponte FFI.
- **Negativas**: GIL impede paralelismo CPU em processo unico (workaround: workers Celery e processos uvicorn multiplos); throughput por CPU inferior a .NET/Rust em rotas IO-bound triviais (irrelevante no perfil de carga atual).
- **Riscos**: dependencia da continuidade do FastAPI (mitigado: projeto consolidado, mantido por Tiangolo + comunidade ativa); regressoes em Pydantic v2 em casos exoticos (mitigado: cobertura de testes nos schemas).

## Referencias

- /Users/rafaeldias/IdeaProjects/calc-3d/docs/planning/03-DESIGN.md (Stack proposta — Backend; Arquitetura macro)
- /Users/rafaeldias/IdeaProjects/calc-3d/docs/planning/03-DESIGN.md (Migracao do codigo atual)
