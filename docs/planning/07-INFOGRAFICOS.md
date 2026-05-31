---
documento: infográficos e diagramas de fluxo
versao: 1.0
data: 2026-05-31
formato: ASCII art (renderiza em qualquer leitor markdown sem dependência)
---

# 07 — INFOGRÁFICOS E DIAGRAMAS DE FLUXO

## INFOGRÁFICO 1 — Arquitetura macro

```
                            ╔══════════════════════╗
                            ║   USUÁRIO (browser)  ║
                            ║   web · mobile · API ║
                            ╚══════════╤═══════════╝
                                       │ HTTPS
                                       │
                          ┌────────────┴────────────┐
                          │  CDN + WAF (Cloudflare) │
                          └────────────┬────────────┘
                                       │
                       ╔═══════════════▼═══════════════╗
                       ║      FastAPI (gateway)         ║
                       ║  ─────────────────────────     ║
                       ║  · auth (JWT)                  ║
                       ║  · rate limit                  ║
                       ║  · pydantic validate           ║
                       ║  · routing                     ║
                       ╚═════╤═════════╤═════════╤══════╝
                             │         │         │
              ┌──────────────┘         │         └──────────────┐
              │                        │                        │
       ╔══════▼══════╗         ╔═══════▼══════╗         ╔═══════▼══════╗
       ║  Project    ║         ║  Calculation ║         ║   Report     ║
       ║  service    ║         ║   service    ║         ║   service    ║
       ║  (CRUD)     ║         ║  (orquestra) ║         ║ (PDF/DXF/IFC)║
       ╚══════╤══════╝         ╚═══════╤══════╝         ╚══════╤═══════╝
              │                        │                       │
              │                ┌───────▼────────┐              │
              │                │  Celery Queue  │              │
              │                │  (cálc > 10s)  │              │
              │                └───────┬────────┘              │
              │                        │                       │
              │         ╔══════════════▼══════════════════╗    │
              │         ║         CORE ENGINE             ║    │
              │         ║  ┌──────┐ ┌──────┐ ┌──────────┐ ║    │
              │         ║  │ FEM  │ │  GEO │ │  DESIGN  │ ║    │
              │         ║  │frame │ │solos │ │NBR/EC/ACI│ ║    │
              │         ║  └──┬───┘ └──┬───┘ └────┬─────┘ ║    │
              │         ║     │        │          │        ║    │
              │         ║  ┌──▼────────▼──────────▼─────┐ ║    │
              │         ║  │   STANDARDS REGISTRY       │ ║    │
              │         ║  │  (versionamento de norma)  │ ║    │
              │         ║  └────────────┬───────────────┘ ║    │
              │         ╚═══════════════╪══════════════════╝    │
              │                         │                       │
              └──────────┬──────────────┴───────────────────────┘
                         │
              ╔══════════▼═════════════════════╗
              ║   POSTGRES (multi-tenant RLS)  ║
              ║   ──────────────────────────   ║
              ║   · projects                    ║
              ║   · elements                    ║
              ║   · calc_results                ║
              ║   · audit_log (append-only)     ║
              ║   ╔════════════════╗            ║
              ║   ║     REDIS      ║            ║
              ║   ║ cache + queue  ║            ║
              ║   ╚════════════════╝            ║
              ╚═════════════════════════════════╝
```

---

## INFOGRÁFICO 2 — Jornada do usuário leigo (E2E)

```
[Acessa landing]
       │
       ▼
[Cria conta] ────► confirma email ──► [login]
                                         │
                                         ▼
                              ┌─── [Dashboard vazio] ───┐
                              │                          │
                              ▼                          ▼
                      [+ Novo projeto]          (volta depois pra ver)
                              │
                              ▼
            ┌─────────────────────────────────────┐
            │  WIZARD (5 passos)                  │
            │  ┌────┐  ┌────┐  ┌────┐  ┌────┐  ┌────┐
            │  │tipo│─►│geom│─►│CEP │─►│SPT │─►│conf│
            │  └────┘  └────┘  └────┘  └────┘  └────┘
            └─────────────────────────────────────┘
                              │
                              ▼
                  [Backend infere e valida]
                  · vento por CEP (NBR 6123)
                  · carga acidental (NBR 6120)
                  · materiais default
                  · combinações (NBR 8681)
                              │
                              ▼
                  [Cálculo enfileirado em Celery]
                              │
                              ▼
              ┌────── FEM ───────┐
              │  · monta matriz   │
              │  · resolve K·u=F  │
              └────────┬──────────┘
                       │
                       ▼
              ┌── DIMENSIONAMENTO ──┐
              │  · NBR 6118 vigas    │
              │  · NBR 6118 pilares  │
              │  · NBR 6122 sapatas  │
              └────────┬─────────────┘
                       │
                       ▼
              ┌──── GEO ────┐
              │ Terzaghi    │
              │ Recalque    │
              └─────┬───────┘
                    │
                    ▼
            ┌── RELATÓRIO ──┐
            │  PDF + JSON   │
            └──────┬────────┘
                   │
                   ▼
          [T-30 Resultado pro usuário]
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
    [download]  [ajusta] [duplica]
```

---

## INFOGRÁFICO 3 — Fluxo interno: 1 cálculo de viga (drill-down NBR 6118)

```
INPUT
─────
  · seção (b, h)
  · vão (L)
  · esforços (Md, Vd) ← vêm do FEM
  · material (fck, fyk)
  · ambiente (CAA → cobrimento)

       │
       ▼
┌──────────────────────┐
│ 1. Verificar domínio │
│    de deformação     │  → NBR 6118 §17.2.2
│    (1 / 2 / 3 / 4)   │
└──────────┬───────────┘
           │
           ▼
┌─────────────────────────┐
│ 2. Cálculo As tracionada│  fórmula §17.2.2
│    As = f(Md, b, d, fcd)│
└──────────┬──────────────┘
           │
           ▼
┌────────────────────────────┐
│ 3. Comparar com As mínima  │  §17.3.5.2.1
│    ρ = As/(b·h)            │  ρ_min = max(0.15%, ωmin·fct/fy)
│    se ρ < ρmin → As = ρmin·b·h
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│ 4. Cisalhamento            │  §17.4
│    VRd2 (biela)            │
│    VSd ≤ VRd2  ?           │
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│ 5. Estribo                 │  §17.4.1.1.1 modelo I
│    Asw,min                 │  §17.4.1.1.3
│    spaçing                 │
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│ 6. ELS flecha              │  §17.3.2
│    flecha total ≤ L/250    │
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│ 7. ELS fissuração          │  §17.3.3
│    wk ≤ 0.3 mm             │
└──────────────┬─────────────┘
               │
               ▼
        OUTPUT (cada step)
        ──────────────────
        · As (cm²) + bitolas
        · Asw + estribo
        · η utilização (%)
        · referência norma + fórmula
        · OK / NOT OK + sugestão
```

---

## INFOGRÁFICO 4 — Fluxo solo → fundação (interação)

```
            ┌─────────────────────────┐
            │   Sondagem (input SPT)   │
            │   · profundidade         │
            │   · NSPT                 │
            │   · tipo de solo         │
            └─────────────┬───────────┘
                          │
                          ▼
            ┌─────────────────────────────────┐
            │   Perfil estratigráfico          │
            │   ─────────────────────────      │
            │   camada 1: 0-2m  argila mole    │
            │   camada 2: 2-5m  areia média    │
            │   camada 3: 5-10m areia compacta │
            │   N.A. = 3.0m                    │
            └─────────────┬────────────────────┘
                          │
                          ▼
        ┌─────────────────┴──────────────────┐
        │                                     │
        ▼                                     ▼
┌────────────────────┐           ┌────────────────────┐
│ Cálculo de         │           │ Cálculo de         │
│ capacidade SAPATA  │           │ capacidade ESTACA  │
│ ──────────────     │           │ ──────────────     │
│ Terzaghi           │           │ Décourt-Quaresma   │
│ Meyerhof           │           │ Aoki-Velloso       │
│ Vesic              │           │ Teixeira           │
│ Brinch-Hansen      │           │                    │
└─────────┬──────────┘           └──────────┬─────────┘
          │                                  │
          ▼                                  ▼
   q_adm (kPa)                       Q_adm,estaca (kN)
          │                                  │
          ▼                                  ▼
   ┌──────────────────────────────────────────┐
   │  Esforços vindos da estrutura (FEM)       │
   │  N, Mx, My por sapata/estaca              │
   └────────────────┬──────────────────────────┘
                    │
                    ▼
       ┌────────────────────────────┐
       │  Verificação NBR 6122       │
       │  ─────────────────────      │
       │  · σ_atuante ≤ q_adm?       │
       │  · recalque admissível?     │
       │  · estabilidade ao tombo?   │
       └────────────┬────────────────┘
                    │
                    ▼
              [✓ ou ⚠ + sugestão]
```

---

## INFOGRÁFICO 5 — Modelo de dados (esquemático)

```
┌─────────────┐         ┌─────────────┐        ┌──────────────┐
│  tenants    │1───────∞│   users     │1──────∞│ projects     │
│─────────────│         │─────────────│        │──────────────│
│ id (uuid)   │         │ id          │        │ id           │
│ name        │         │ email       │        │ tenant_id    │
│ plan        │         │ tenant_id   │        │ owner_id     │
│ created_at  │         │ role        │        │ name         │
└─────────────┘         └─────────────┘        │ usage_type   │
                                                │ cep          │
                                                │ standards    │
                                                │ created_at   │
                                                └──────┬───────┘
                                                       │
                                                       │1
                                                       │
                                       ┌───────────────┴──────────────┐
                                       │                              │
                                       ▼∞                             ▼∞
                              ┌────────────────┐            ┌──────────────────┐
                              │ elements       │            │ load_cases       │
                              │────────────────│            │──────────────────│
                              │ id             │            │ id               │
                              │ project_id     │            │ project_id       │
                              │ type (FK)      │            │ type             │
                              │ material_id    │            │ value (JSONB)    │
                              │ geometry(JSONB)│            │ source (manual,  │
                              │ supports       │            │  inferred, etc)  │
                              └────────┬───────┘            └──────────────────┘
                                       │
                                       │∞
                                       │
                              ┌────────▼─────────┐         ┌──────────────────┐
                              │ calc_results     │1──────∞│ audit_log        │
                              │──────────────────│         │──────────────────│
                              │ id               │         │ id               │
                              │ project_id       │         │ result_id        │
                              │ element_id       │         │ user_id          │
                              │ standard_version │         │ action           │
                              │ values (JSONB)   │         │ payload_hash     │
                              │ status           │         │ engine_version   │
                              │ computed_at      │         │ created_at       │
                              └──────────────────┘         └──────────────────┘

┌──────────────┐                ┌────────────────┐
│ soil_profiles│                │ soil_layers    │
│──────────────│1──────────────∞│────────────────│
│ id           │                │ id             │
│ project_id   │                │ profile_id     │
│ water_table  │                │ depth_top      │
│ created_at   │                │ depth_bottom   │
└──────────────┘                │ soil_type      │
                                │ properties JSONB│
                                └────────────────┘
```

---

## INFOGRÁFICO 6 — Pipeline de release

```
┌─────────────┐
│  feature/X  │
└──────┬──────┘
       │ push
       ▼
┌─────────────────┐         ┌─────────────────┐
│ GitHub Actions  │ ──fail──► [bloqueia merge]│
│  · ruff lint    │         └─────────────────┘
│  · mypy strict  │
│  · pytest       │
│  · cobertura    │
│   > 80% (core)  │
└────────┬────────┘
         │ pass
         ▼
   ┌──────────────┐
   │ PR review    │
   │ (Artemis)    │
   └──────┬───────┘
          │ approve
          ▼
   ┌──────────────┐
   │ merge → main │
   └──────┬───────┘
          │
          ▼
   ┌─────────────────┐
   │ Deploy staging  │ ──► smoke test ──► OK?
   │  (auto)         │                     │
   └─────────────────┘                     │ sim
                                           ▼
                                  ┌─────────────────┐
                                  │ tag release     │
                                  │ vN.M.K          │
                                  └────────┬────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │ Deploy prod     │
                                  │ (manual click)  │
                                  └────────┬────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │ Sentry watch    │
                                  │ Prometheus      │
                                  │ rollback se P0  │
                                  └─────────────────┘
```

---

## INFOGRÁFICO 7 — Relação entre as fases do roadmap

```
   Fase 0          Fase 1          Fase 2          Fase 3
 (jun-jul/26)   (ago-set/26)   (out-dez/26)    (jan-mai/27)
    │               │               │               │
    │               │               │               │
    ▼               ▼               ▼               ▼
┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐
│  base  │────►│  MVP   │────►│  MVP   │────►│  v1.0  │
│ técnica│     │concreto│     │completo│     │   GA   │
│ + auth │     │ + sapa │     │+ aço   │     │+ ACI   │
│        │     │ + viga │     │+ madeira│    │+ sismo │
│        │     │ + pilar│     │+ pro   │     │+ ssi   │
│        │     │ + geo  │     │+ IFC   │     │+ DXF   │
│        │     │ básica │     │+ pago  │     │+ studio│
└────────┘     └────────┘     └────────┘     └────────┘
                                                    │
                                                    ▼
                                              ┌──────────┐
                                              │ visão    │
                                              │ Fase 4+  │
                                              │ ─────────│
                                              │ AI       │
                                              │ 3D opt   │
                                              │ on-prem  │
                                              │ mobile   │
                                              └──────────┘
```
