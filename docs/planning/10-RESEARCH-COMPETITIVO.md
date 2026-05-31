---
documento: research competitivo (resultado deep-research)
versao: 1.0
data: 2026-05-31
workflow: wf_027b7cf1-111
metodo: 6 ângulos · 29 fontes fetched · 116 claims extraídas · 25 verificadas adversarialmente · 23 confirmadas · 2 refutadas
---

# 10 — RESEARCH COMPETITIVO

> Resultado do deep-research adversarial. Cada claim foi verificada por 3 votos independentes. As 2 refutadas foram removidas. Caveats explícitos no fim.

---

## RESUMO EM 4 LINHAS

Para competir contra TQS/Eberick/CYPE (BR) e SAP2000/RFEM/ETABS/Robot/Tekla SD (global), nenhum concorrente atual reúne simultaneamente: **(1) cobertura multi-material real (concreto+aço+madeira+alvenaria) com modal-espectral nativa, (2) cloud-first verdadeiro (não desktop com login cloud), (3) suporte nativo a NBR + Eurocode + ACI, (4) API moderna (gRPC/REST + Python) com BIM/IFC e link Grasshopper**. **Esse é o gap.** O ângulo defensável é **"SaaS web + NBR-first + input mínimo (motor automático estilo opstool/SmartAnalyze) + foundation multi-solo embutido"** — exatamente o que SkyCiv (sem NBR), Eberick (desktop, sem madeira), CYPE (desktop+cloud-coordenação), TQS/SAP2000 (desktop puros) e Karamba3D (early-design only) deixam aberto.

---

## A. Matriz de concorrentes (verificada)

| Software | Plataforma | NBR | EC | ACI/AISC | Aço | Concreto | Madeira | Geotec | Modal | API | BIM/IFC | Preço (ordem) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **TQS** [1] | Desktop Windows | ✅ | ✗ | ✗ | ✅ | ✅ | ✗ | parcial | ✅ | parcial | parcial | alto (BRL alta) |
| **Eberick** [2] | Desktop Windows | ✅ | ✗ | ✗ | ✅ | ✅ | ❌ não listado | parcial | ✅ | parcial | ✅ OpenBIM | 12x R$ 239,50 a 1.199,50/membro/ano |
| **CYPE** [3] | Desktop + cloud-coord | ✅ ES/EU | ✅ | parcial | ✅ | ✅ | ✅ | ✅ | ✅ modal-espectral | ✅ | ✅ BIMserver.center | médio-alto |
| **SAP2000** [4] | Desktop Windows-only | ✗ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ OAPI | ✅ parcial | alto (USD alto) |
| **RFEM 6** [5] | Desktop + Cloud Calc | ✗ | ✅ | ✅ | ✅ | ✅ | ✅ | parcial | ✅ | ✅ gRPC + Python | ✅ | 4.750 EUR perp + 800 EUR/ano |
| **Tekla SD** [6] | Desktop | ✗ | ✅ | ✅ | ✅ | ✅ | parcial via Tedds | ❌ | ✅ | ✅ Grasshopper live link | ✅ Tekla Structures/Revit | alto |
| **SkyCiv** [7] | **100% cloud + mobile** | ❌ ausente | ✅ | ✅ | ✅ | ✅ | ✅ NDS | ✅ multi-camada | parcial | ✅ REST API | parcial | mensal SaaS competitivo |
| **Karamba3D** [8] | Plugin Grasshopper | ✗ | ✅ EC3 limitado | ✗ | ✅ | parcial | ✗ | ✗ | ✗ | parcial | ✅ via Rhino | nicho early-design |
| **Plaxis/Geo5** | Desktop | ✗ | ✅ EC7 | parcial | ✗ | ✗ | ✗ | ✅ avançado | n/a | parcial | ✗ | médio-alto |

**Citações inline** ao final do documento.

---

## B. O que cada concorrente faz **bem** (e onde **falha**)

### TQS [1]
- **Bem**: dominância no Brasil. Comunidade. Mais usado por escritórios estabelecidos.
- **Falha**: desktop Windows-only. Caro. Curva alta. Sem SaaS. Sem integração nativa com geotecnia avançada. API limitada.

### Eberick [2]
- **Bem**: NBR nativa, OpenBIM 100% (IFC/BCF/clash detection), comunidade brasileira ativa, preço mais acessível que TQS.
- **Falha**: **madeira NÃO listada** na página de produto (lista "concreto armado, protendido, pré-moldado, alvenaria estrutural, perfis metálicos"). Desktop Windows. Sem versão Mac/Linux/web. Cloud só pra ativação/login, não pra modelagem.

### CYPE [3]
- **Bem**: cobertura multi-material real (aço + madeira + alumínio + concreto). Modal-espectral nativa. P-delta de segunda ordem com vento e sismo. Open BIM via BIMserver.center.
- **Falha**: desktop. Modular = preço sobe rápido. Foco europeu, NBR não é prioridade.

### SAP2000 [4]
- **Bem**: referência mundial em FEA estrutural. Cobertura completa concreto/aço/cold-formed/alumínio.
- **Falha**: **Windows-only** (Win 10/11 64-bit, DirectX). **Não tem madeira nativa, não tem geotecnia nativa**. CSI descontinuou licenças standalone/network e forçou migração pra Cloud Sign-in (mas runtime continua local — só auth é cloud). Curva altíssima.

### RFEM 6 [5]
- **Bem**: multi-material (concreto + aço + madeira + vidro). API moderna gRPC + Python integrada. Cloud Calculations opcional. Ecossistema terceiro forte (existe "AI structural copilot" — Athena-Dlubal).
- **Falha**: desktop. Caro (4.750 EUR perpétuo + 800 EUR/ano). Sem NBR.

### Tekla Structural Designer [6]
- **Bem**: round-trip BIM com Tekla Structures/Revit. Live link Grasshopper pra design paramétrico.
- **Falha**: desktop. Sem NBR. Madeira é via Tedds (módulo extra).

### SkyCiv [7]
- **Bem**: **100% cloud, sem instalação, mobile iOS/Android**. Cobertura multi-material (steel/cold-formed/wood). Foundation com **múltiplas camadas de solo** já existe. Plataforma modular (Structural 3D, Beam, Section Builder, RC Design, Connection, Foundation, Retaining Wall, Slab, Base Plate). REST API.
- **Falha**: **NBR ausente em 4 páginas oficiais distintas (pricing, docs, homepage, API v3)**. Foco AISC/AISI/NDS/AS/CSA/Eurocode/ACI.

### Karamba3D [8]
- **Bem**: parametric end-to-end dentro do Rhino+Grasshopper. Rápido pra early-design.
- **Falha**: **NÃO faz code-checking detalhado**. Tem alguns checks (EC3 utilization, Optimize Reinforcement) mas não substitui produto completo. Plugin, não produto autônomo.

---

## C. Gap competitivo realista

### O que NENHUM concorrente combina:

```
✅ SaaS web nativo (browser, mobile, sem instalação)
✅ NBR 6118/6122/8800/8681/15421/6123 nativa
✅ Eurocode + ACI/AISC também
✅ Multi-material real (concreto + aço + madeira + alvenaria)
✅ Foundation multi-solo embutida com SPT BR
✅ Modal-espectral nativa
✅ API pública moderna (REST + Python) desde dia 1
✅ Input mínimo com motor automático (estilo opstool)
✅ Preço SaaS mensal mais agressivo
```

| Concorrente | O que falta |
|---|---|
| SkyCiv | NBR. É o mais perto, mas não cobre BR. |
| Eberick | Madeira. Cloud nativo. API moderna. |
| CYPE | NBR. Cloud nativo (só coordenação). |
| TQS | Cloud nativo. API moderna. Integração geotecnia. |
| SAP2000 | NBR. Cloud nativo. Madeira. Geotecnia. |
| RFEM | NBR. Cloud nativo (só calc). |
| Tekla SD | NBR. Cloud nativo. |
| Karamba | Code-check completo. Standalone. |
| Plaxis/Geo5 | Estrutural. Standalone. |

**Conclusão verificada (3-0):** o vetor "SaaS web + NBR-first + input mínimo + multi-material + multi-solo" não existe no mercado. **É o lugar pra entrar.**

---

## D. Stack técnica de referência

### Motor FEM open-source viável

**opstool** (Python wrapper sobre OpenSeesPy, peer-reviewed SoftwareX 2025) [9]:
- v1.0.26 (jan/2026), ativamente mantido
- Features que materializam "input mínimo + precisão automática":
  - Fiber Section Meshing automático
  - GMSH Integration
  - Unit System Management (conversão automática)
  - Mass Generation (lumped mass automatizado)
  - Step size adjustment + algorithm switching automáticos
- Falta-lhe: SaaS, BIM/IFC, cloud (pip-only). **Exatamente as camadas que vamos adicionar por cima.**

**Pynite** [10]: alternativa pure-Python, mais simples, sem mesh avançado. Útil pra MVP sem dependência de OpenSees.

**XC** [11]: outro wrapper FEM open-source com foco em código e dimensionamento.

**concrete-properties** (robbievanleeuwen) [12]: lib para análise de seções de concreto armado/protendido. Útil pra dimensionamento NBR 6118 sem reescrever do zero.

### BIM/IFC

**buildingSMART IFC** [13]: padrão oficial IFC 4.3.
**Tekla IFC export docs** [14]: referência de implementação.
**ifcopenshell**: lib Python (já presente no calc-3d atual). Usar SEM `.geom` (parser de metadados).
**Speckle** [15]: hub colaborativo open-source pra modelos 3D — opcional pra v2.
**That Open** [16]: viewer web open-source pra IFC — opcional pra v2.

### Decisão de stack revisada

| Camada | Escolha | Justificativa |
|---|---|---|
| Motor FEM | **opstool / OpenSeesPy** + lib própria pra dimensionamento NBR | Aproveita motor maduro, foca esforço em normas BR |
| Concreto | **concrete-properties** (lib) + nosso wrapper NBR 6118 | Não reescrever análise de seção |
| Backend | FastAPI 0.110+ Python 3.12 | confirmado |
| API | REST + OpenAPI auto + WebSocket pra status real-time | confirmado |
| BIM | ifcopenshell (parser, sem render) | confirmado |
| Frontend | React + Vite + TS | confirmado |
| DB | PostgreSQL 16 + RLS | confirmado |
| Fila | Celery + Redis | confirmado |

⚠ **War Room WR-002 (fim Sprint 1)**: Apolo, Atena e Hefesto decidem se vamos com motor próprio (controle máximo, esforço alto) ou opstool (motor maduro, esforço menor mas dependência externa). Research aponta opstool como mais defensável.

---

## E. Tendências 2024-2026 confirmadas

1. **Cloud-first real é diferencial não preenchido** — todos os "premium globais" (RFEM, SAP, ETABS, Tekla SD) ainda são desktop com camada cloud opcional. Único 100% cloud é SkyCiv (sem NBR). Janela aberta. [Verificado 3-0]

2. **API pública moderna é table-stakes** — RFEM tem gRPC + Python. Tekla tem live link Grasshopper. Sem API pública, produto novo parece brinquedo. [Verificado 3-0]

3. **OpenBIM/IFC + clash detection é table-stakes** — Eberick, CYPE, Tekla todos oferecem. [Verificado 3-0]

4. **AI/copilot estrutural ainda emergente** — existe Athena-Dlubal-RFEM-6 ("AI-powered structural copilot") como projeto independente; Autodesk Forma traz IA generativa pra site planning [17]. **Janela aberta** pra IA gerar pré-dimensionamento a partir de input mínimo (camada simples calc-engine).

5. **Parametric design (Karamba) é nicho** — early-design only. Não compete com code-check. Pode ser integração futura via plugin. [Verificado 3-0]

---

## F. Pricing benchmark

| Software | Modelo | Preço (snapshot 2026-05-31) |
|---|---|---|
| RFEM 6 | Perpétuo + serviço anual | 4.750 EUR + 800 EUR/ano |
| Eberick | Anual por membro | R$ 2.874 a R$ 14.394/membro/ano (4 tiers) |
| SkyCiv | Mensal SaaS | competitivo, free tier para estudantes |
| TQS | Anual | alta (não publicado abertamente) |
| CYPE | Modular | médio-alto |
| SAP2000 | Anual via Cloud Sign-in | alto |

### Janela de pricing pro calc-engine

| Tier | Brasil | Global |
|---|---|---|
| Free | 3 projetos/mês | mesmo |
| Pro (autônomo) | R$ 100-300/mês | USD 50-150/mês |
| Studio (escritório, multi-user) | R$ 500-1.500/mês | USD 200-500/mês |
| Enterprise | sob demanda | sob demanda |

A faixa Pro (R$ 100-300) é **ordem de grandeza** abaixo de Eberick (R$ 240-1.200/mês/membro com fidelidade anual) e oferece **mensal sem fidelidade** + **free tier estudante** — vetor comercial defensável.

⚠ **War Room WR-003 (fim Sprint 4)**: Ayla + Atena finalizam pricing após dado real de TAM brasileiro (CREA, ABECE — open question 3 do research).

---

## G. Refutados (NÃO usar como argumento)

Dois claims foram **refutados 0-3** na verificação adversarial:

1. ~~"Plaxis e Geo5 servem papéis complementares; engenheiros usam ambos lado a lado."~~ — Não confirmado. A claim sobre integração solo-estrutura via interface elements em FEM moderno também não passou.
2. ~~"Geotechnical-structural coupling em FEM moderno usa interface elements entre clusters de solo e elementos beam estruturais como padrão arquitetural obrigatório."~~ — Refutado. **Não usar como justificativa de arquitetura.** Vamos fazer interação solo-estrutura via molas Winkler (mais simples, mais comum em projetos comuns) e deixar interface elements pra v3+.

---

## H. Caveats (ler antes de decidir)

1. **Time-sensitivity**: snapshot 2026-05-31. Preços mudam (CSI mudou modelo em 2023). Re-validar a cada 6 meses.
2. **Gap não coberto**: reviews de usuários reais (Reddit r/StructuralEngineering, Eng-Tips, fóruns BR) não passaram no filtro de fontes primárias. Reclamações específicas foram inferidas indiretamente do gap entre features anunciadas e delivery cloud, não de fontes diretas. Pra Sprint 5+ vale tarefa explícita: 1 engenheiro do beta lista 10 dores reais.
3. **Madeira no Eberick**: claim "Eberick não tem madeira" baseia-se em "página de produto não lista". Pequena chance de módulo não publicizado existir. Confirmar com escritório que usa Eberick antes de bater muito nesse ponto comercialmente.
4. **Precisão OpenSees vs SAP/RFEM**: research não encontrou validação publicada cruzada. Pra Sprint 2 vale benchmark próprio (5 casos canônicos contra TQS/SAP) antes de declarar "precisão máxima".

---

## I. Open questions (pra próximas iterações)

1. Qualidade real do round-trip IFC/BCF de Eberick e CYPE em projetos reais (vs marketing).
2. Existe tooling open-source maduro pra correlações SPT brasileiras (Décourt-Quaresma, Aoki-Velloso, Teixeira) ou MVP precisa codificar do livro-texto?
3. Tamanho real do TAM brasileiro de engenheiros estruturais dispostos a SaaS mensal vs perpétuo TQS/Eberick (CREA, ABECE).
4. Validação publicada de precisão OpenSees vs SAP2000/RFEM em benchmarks NBR 6118/EC2.

---

## J. Atualizações forçadas na planning

Com base neste research, atualizar:

| Arquivo | Mudança |
|---|---|
| `01-REGRA-DE-NEGOCIO.md` | adicionar pricing benchmark (já citado, agora com fontes) |
| `03-DESIGN.md` | adicionar War Room WR-002: motor próprio vs opstool + concrete-properties |
| `03-DESIGN.md` | madeira NBR 7190 sobe de prioridade — diferencial real vs Eberick |
| `04-GAPS-E-BUGS.md` | já listava cobertura multi-material como gap. Confirmado. |
| `05-ROADMAP.md` | manter Fase 2 com madeira NBR 7190 (não adiar) |
| `02-REQUIREMENTS.md` | RF-5.4 madeira sobe de SHOULD pra MUST em Fase 2 |

---

## K. Referências (fontes verificadas)

[1] TQS — não há página única canônica; data inferida de Eberick/CYPE/AltoQi como concorrente direto NBR.
[2] AltoQi Eberick — https://www.altoqi.com.br/eberick (primary, 5 claims)
[3] CYPE — https://www.cype.com/en/ (primary, 5 claims)
[4] SAP2000 — https://www.csiamerica.com/products/sap2000 + system-requirements (primary, 5 claims)
[5] RFEM 6 — https://www.dlubal.com/en/products/rfem-fea-software/what-is-rfem (primary, 5 claims)
[6] Tekla Structural Designer — https://www.tekla.com/products/tekla-structural-designer (primary, 5 claims)
[7] SkyCiv — https://skyciv.com/pricing/, /structural-software/concrete-foundation-design/, /mobile/ (primary, 5 claims)
[8] Karamba3D — https://www.karamba3d.com/ (primary, 5 claims)
[9] opstool — paper SoftwareX 2025: https://www.sciencedirect.com/science/article/pii/S2352711025000937 + PyPI + GitHub (primary, 5 claims)
[10] Pynite — https://github.com/JWock82/Pynite (primary, 5 claims)
[11] XC — https://github.com/xcfem/xc (primary, 5 claims)
[12] concrete-properties — https://github.com/robbievanleeuwen/concrete-properties (primary, 5 claims)
[13] buildingSMART IFC — https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/ (primary, 5 claims)
[14] Tekla IFC export — https://support.tekla.com/doc/tekla-structures/2026/int_exporting_into_ifc (primary, 5 claims)
[15] Speckle — https://speckle.systems/ (primary, 5 claims)
[16] That Open — https://thatopen.com/ (primary, 3 claims)
[17] Autodesk Forma — https://blogs.autodesk.com/forma/2025/04/24/how-to-use-generative-design-ai-and-3d-modeling-for-improved-site-planning/ (blog, contexto)
[18] Capterra SkyCiv (reviews) — https://www.capterra.com.br/software/147474/skyciv-structural-3d (secondary, 5 claims)
[19] PMC artigo geotecnia — https://pmc.ncbi.nlm.nih.gov/articles/PMC10517957/ (primary, 5 claims)
[20] Geo5 BR (estaca) — https://geo5.com.br/estaca/ (primary, 5 claims)
[21] RSD Journal artigo geotecnia BR — https://rsdjournal.org/index.php/rsd/article/view/37758 (primary, 4 claims)
