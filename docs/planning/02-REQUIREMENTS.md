---
documento: requirements
versao: 1.0
data: 2026-05-31
escopo: MVP (até v1.0) — recortes pra v1.5/v2 marcados [v1.5] [v2]
---

# 02 — REQUISITOS

## Convenções

- **RF** = requisito funcional · **RNF** = requisito não-funcional
- **MUST** = bloqueia release · **SHOULD** = forte mas não bloqueia · **MAY** = opcional
- **[L]** = camada Leigo · **[P]** = camada Pro · **[L+P]** = ambas

---

## Requisitos Funcionais

### RF-1 — Autenticação e contas
- **RF-1.1 MUST** [L+P] Login email/senha com confirmação por email
- **RF-1.2 MUST** [L+P] Recuperação de senha
- **RF-1.3 SHOULD** [L+P] OAuth Google
- **RF-1.4 MUST** [P] Workspaces multi-usuário (tier Studio)
- **RF-1.5 MUST** [L+P] RBAC: owner, editor, viewer

### RF-2 — Projetos
- **RF-2.1 MUST** [L+P] CRUD de projeto (nome, cliente, endereço, CEP, descrição)
- **RF-2.2 MUST** [L+P] Versionamento de projeto (snapshot a cada cálculo)
- **RF-2.3 SHOULD** [P] Branching de projeto (estudo de alternativas)
- **RF-2.4 MUST** [L+P] Soft delete + retenção 90 dias

### RF-3 — Wizard de input mínimo (camada leigo)
- **RF-3.1 MUST** [L] Tipo de obra (residencial uni/multi, galpão, comercial, muro de arrimo)
- **RF-3.2 MUST** [L] Geometria simplificada (nº pavimentos, pé-direito, planta retangular dimensões)
- **RF-3.3 MUST** [L] Inferência de carga acidental por NBR 6120 a partir do tipo de uso
- **RF-3.4 MUST** [L] Inferência de vento por CEP → vb (NBR 6123) + topografia simplificada
- **RF-3.5 SHOULD** [L] Inferência de zona sísmica por CEP (NBR 15421) — v1.5
- **RF-3.6 MUST** [L] Sondagem opcional: SPT por camada (entrada simples) OU "sem sondagem → premissa conservadora explícita"

### RF-4 — Editor paramétrico (camada pro)
- **RF-4.1 MUST** [P] Definir geometria por nós + barras + elementos (input tabular)
- **RF-4.2 MUST** [P] Materiais customizados (concreto, aço, madeira) com curva tensão-deformação
- **RF-4.3 MUST** [P] Combinações de carga manuais (ELU/ELS)
- **RF-4.4 MUST** [P] Override de qualquer coeficiente normativo (γc, γs, γf, ψ) com justificativa
- **RF-4.5 SHOULD** [P] Importação IFC 4.x (parser de geometria, sem render) — v1.5
- **RF-4.6 SHOULD** [P] Importação CSV/JSON (replicar `tqs_data_importer.py` atual)

### RF-5 — Motor de cálculo estrutural
- **RF-5.1 MUST** Análise estática linear (frame 3D)
- **RF-5.2 MUST** Dimensionamento concreto armado NBR 6118: vigas (flexão simples + cisalhamento), pilares (flexo-compressão), lajes maciças (flexão + flecha)
- **RF-5.3 MUST** Dimensionamento aço NBR 8800: tração, compressão, flexão, ligações simples (parafusadas + soldadas)
- **RF-5.4 SHOULD** Dimensionamento madeira NBR 7190 — Fase 2 (MUST)
- **RF-5.5 MUST** Dimensionamento Eurocode 2 (concreto), Eurocode 3 (aço)
- **RF-5.6 SHOULD** Dimensionamento ACI 318 (concreto), AISC 360 (aço) — v1.5
- **RF-5.7 SHOULD** Análise não-linear física (concreto fissurado) — v1.5
- **RF-5.8 SHOULD** Análise modal + espectro de resposta NBR 15421 — v2
- **RF-5.9 MUST** Verificação ELS: flecha, fissuração, vibração

### RF-6 — Motor geotécnico
- **RF-6.1 MUST** Capacidade de carga sapata: Terzaghi, Meyerhof, Vesic, Brinch-Hansen
- **RF-6.2 MUST** Capacidade de carga estaca: Décourt-Quaresma, Aoki-Velloso (a partir de SPT)
- **RF-6.3 MUST** Recalque imediato sapata: elástico (Boussinesq)
- **RF-6.4 SHOULD** Recalque por adensamento: Terzaghi 1D — v1.5
- **RF-6.5 MUST** Perfil estratigráfico: N camadas, cada uma com tipo+propriedades
- **RF-6.6 MUST** Biblioteca de tipos de solo brasileiros (12+ tipos com faixa de propriedades)
- **RF-6.7 SHOULD** Interação solo-estrutura: molas de Winkler na fundação alimentando análise estrutural — v1.5
- **RF-6.8 MUST** Cobertura completa NBR 6122 pros tipos de fundação suportados
- **RF-6.9 MUST** Tipos de fundação: sapata isolada, sapata corrida, radier, bloco sobre estaca, estaca pré-moldada, estaca hélice contínua, tubulão (já existem em código, refatorar)

### RF-7 — Cargas
- **RF-7.1 MUST** Carga permanente (peso próprio automático + cargas adicionais)
- **RF-7.2 MUST** Carga acidental NBR 6120 (tabela embutida por uso)
- **RF-7.3 MUST** Carga de vento NBR 6123 (vb por CEP, topografia, rugosidade)
- **RF-7.4 SHOULD** Carga sísmica NBR 15421 — v1.5
- **RF-7.5 MUST** Combinações automáticas ELU/ELS (NBR 8681)

### RF-8 — Saídas
- **RF-8.1 MUST** Relatório técnico PDF: capa + memória de cálculo passo-a-passo + citações de norma + tabelas + gráficos 2D
- **RF-8.2 MUST** JSON estruturado da resposta completa (estado, esforços, dimensionamento)
- **RF-8.3 SHOULD** Exportação DXF de planta de fôrma e armação — v1.5
- **RF-8.4 SHOULD** Exportação IFC do modelo dimensionado — v2
- **RF-8.5 MUST** Lista de materiais (volume concreto, peso aço, área fôrma)

### RF-9 — API pública (tier Pro+)
- **RF-9.1 MUST** REST API com OpenAPI spec
- **RF-9.2 MUST** API key por usuário com escopo
- **RF-9.3 SHOULD** Webhook no fim de cálculo longo
- **RF-9.4 MAY** Plugin Grasshopper — v2

### RF-10 — Auditoria e compliance
- **RF-10.1 MUST** Log imutável de cada cálculo: usuário, timestamp, hash dos inputs, versão do motor, versão da norma aplicada
- **RF-10.2 MUST** Versionamento de norma (NBR 6118:2014 atual; futuras = nova versão do motor sem invalidar antigas)
- **RF-10.3 MUST** Citação inline em cada resultado: "verificação X conforme NBR 6118:2014, item 17.3.2.2"

---

## Requisitos Não-Funcionais

### RNF-1 — Performance
- **RNF-1.1 MUST** Cálculo de pórtico até 200 nós retorna em < 5s (p95)
- **RNF-1.2 MUST** Cálculo de wizard leigo (residência simples) retorna em < 30s (p95)
- **RNF-1.3 MUST** API respeita rate limit 60 req/min (Free), 600 req/min (Pro). Implementacao via slowapi + Redis em Sprint 1 (nao S22).

### RNF-2 — Disponibilidade
- **RNF-2.1 MUST** SLO 99.5% (≈ 3.6h/mês de downtime)
- **RNF-2.2 MUST** Backup diário de banco com retenção 30 dias. Implementacao em Sprint 0: pg_basebackup + retencao 30d documentada em docs/runbooks/backup.md.

### RNF-3 — Segurança
- **RNF-3.1 MUST** TLS 1.3 obrigatório
- **RNF-3.2 MUST** Senhas com bcrypt/argon2
- **RNF-3.3 MUST** OWASP Top 10: SQLi, XSS, CSRF, IDOR cobertos
- **RNF-3.4 MUST** Isolamento multi-tenant: tenant nunca vê dado de outro
- **RNF-3.5 MUST** pen test EXTERNO antes de v1.0; ZAP baseline scan automatizado no CI desde S0 (MUST).

### RNF-4 — Precisão numérica
- **RNF-4.1 MUST** Erro relativo < 1% para grandezas continuas (As, Md, Vd, q_adm, recalque). Para grandezas discretas (bitola, espacamento de estribo, numero de barras): comparacao categorica — igual OU dentro de ±1 unidade da tabela comercial.
- **RNF-4.2 MUST** Suite de testes com casos canônicos por norma (cada cálculo tem teste fixture com input/output verificado)
- **RNF-4.3 MUST** Bench cruzado contra software de referência (TQS/SAP2000) em pelo menos 10 casos por norma — antes do release

### RNF-5 — Manutenibilidade
- **RNF-5.1 MUST** Cobertura de testes > 80% no `core` (motor de cálculo)
- **RNF-5.2 MUST** Type hints em 100% do código Python
- **RNF-5.3 MUST** Lint: ruff + mypy strict no CI
- **RNF-5.4 MUST** Cada norma é uma classe/módulo separado (nunca acoplar lógica de NBR e Eurocode no mesmo arquivo)

### RNF-6 — Escalabilidade
- **RNF-6.1 MUST** Stateless API (escala horizontal)
- **RNF-6.2 MUST** Cálculos longos (> 10s) vão pra fila assíncrona (Celery/RQ)
- **RNF-6.3 SHOULD** Multi-region até v2

### RNF-7 — Observabilidade
- **RNF-7.1 MUST** Logs estruturados (JSON) com request_id e tenant_id
- **RNF-7.2 MUST** Métricas Prometheus: latência por endpoint, fila de cálculo, erros
- **RNF-7.3 SHOULD** Tracing distribuído (OpenTelemetry)

### RNF-8 — Documentação
- **RNF-8.1 MUST** Docstring em todos os cálculos com fórmula + referência de norma
- **RNF-8.2 MUST** OpenAPI/Swagger autogerado
- **RNF-8.3 MUST** Manual técnico (web) explicando cada método com exemplos resolvidos

### RNF-9 — Acessibilidade (frontend)
- **RNF-9.1 MUST** WCAG 2.1 AA: contraste, ARIA labels, navegacao teclado
- **RNF-9.2 MUST** axe-core no CI, build falha em violacao P0/P1
- **RNF-9.3 SHOULD** Screen reader smoke test (NVDA/VoiceOver) em wizard

### RNF-10 — Performance frontend
- **RNF-10.1 MUST** LCP < 2.5s, INP < 200ms
- **RNF-10.2 MUST** Bundle inicial < 250kb gzip por chunk
- **RNF-10.3 MUST** Lighthouse CI: performance + a11y > 90

### RNF-11 — Browsers suportados
- **RNF-11.1 MUST** Chrome/Edge/Safari/Firefox ultimas 2 versoes
- **RNF-11.2 MUST** Mobile: iOS Safari 16+, Android Chrome 110+
- **RNF-11.3 SHOULD** Graceful degradation IE11 ausente (mensagem de upgrade)

---

## Fora do escopo (explícito)

- ❌ Renderização 3D no produto (sem Three.js, sem viewer interativo no MVP)
- ❌ GUI desktop (PyQt6 sai, definitivo)
- ❌ Detalhamento gráfico drag-and-drop (input é tabular ou wizard)
- ❌ FEM avançado: cascas curvas, contato, fluido-estrutura
- ❌ Cálculo de obra de arte especial (ponte, túnel) no MVP
- ❌ Suporte a normas que não sejam NBR/Eurocode/ACI no MVP
