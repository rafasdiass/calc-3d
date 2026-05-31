---
documento: pilar frontend
versao: 1.0
data: 2026-05-31
status: proposta tecnica (pendente decisoes War Room)
escopo: MVP (F0-F3) + extensoes ate v1.5
referencias:
  - 02-REQUIREMENTS.md (RF-1 a RF-10, RNF-1, RNF-3, RNF-7)
  - 03-DESIGN.md (stack proposta, multi-tenancy, fluxos)
  - 06-FLUXOS-DE-TELA.md (T-01 a T-60, estados de erro)
  - 08-SPRINTS.md (S0-T16, S0-T17, dependencias FE)
---

# 11 — FRONTEND (PILAR)

> Documento de pilar do front-end. Decisoes finais saem em War Room — secao **N** lista o que ainda esta aberto. Tudo aqui referencia a planning canonica; nao duplico requisito nem fluxo de tela.

---

## A. Decisao de stack

**Stack proposta:** React 18 + Vite 5 + TypeScript 5.4 + TanStack Query v5 + **shadcn/ui** (recomendado sobre Mantine).

### Justificativa

| Item | Escolha | Por que |
|---|---|---|
| Build | Vite 5 | HMR sub-segundo, esbuild + rollup, zero config relevante. Compativel com React 18 SWC. |
| Linguagem | TypeScript 5.4 strict | Espelha `mypy strict` do backend (RNF-5.3). Type safety de ponta a ponta com OpenAPI gerado. |
| Framework UI | React 18 | Concurrent rendering ajuda nas tabelas de resultado de T-30 e na arvore do editor PRO (T-20). Ecossistema compativel com TanStack/RHF/shadcn. |
| Server state | TanStack Query v5 | Cache, retry, background refetch, optimistic updates. Reduz codigo de fetch em ~70% vs `useEffect`. |
| UI lib | shadcn/ui | Radix headless + Tailwind, copia-cola (sem lock-in de versao), acessibilidade WCAG 2.1 AA built-in via Radix. Aderente a `03-DESIGN.md` que ja cita "shadcn/ui ou Mantine". |
| Estilo | Tailwind CSS 3 | Tokens via CSS vars, dark mode por classe, purge agressivo (bundle pequeno). |

### Por que NAO Next.js

- Produto e **SaaS autenticado** (T-04 dashboard pra frente — ver `06-FLUXOS-DE-TELA.md`). SSR nao agrega valor: nao ha SEO em pagina logada, nao ha `getServerSideProps` que justifique o framework.
- Landing publica (T-01) e simples e estatica — pode ser servida pelo proprio Vite ou (eventual) por um CMS headless externo (ver decisao em N).
- Next.js Server Actions + Edge runtime aumentam superficie de complexidade que nao precisamos: o backend e FastAPI (`03-DESIGN.md` secao "Stack proposta"), nao Node.
- SPA pura via Vite tem build mais previsivel, deploy mais barato (estatico em CDN), e e o que o time backend Python vai conseguir manter sem virar especialista em runtime Node.
- Migrar pra Next.js depois (se um dia precisar de SSR/RSC pra landing/blog) e factivel — o oposto (sair de Next) e doloroso.

---

## B. Estrutura de pastas

Layout proposto pra `apps/web/` (espelha o `apps/api/` ja descrito em `03-DESIGN.md`):

```
apps/web/
├── public/
│   ├── favicon.svg
│   ├── og-image.png
│   └── robots.txt
├── src/
│   ├── api/                     # client gerado + wrappers
│   │   ├── generated/           # ⚠ gerado por openapi-typescript-codegen, nunca editar
│   │   │   ├── core/
│   │   │   ├── models/
│   │   │   └── services/
│   │   ├── client.ts            # axios/fetch instance + interceptors (auth, retry)
│   │   ├── query-keys.ts        # chaves canonicas TanStack Query
│   │   └── errors.ts            # mapeamento 401/403/422/5xx
│   ├── components/              # primitivos compartilhados
│   │   ├── ui/                  # shadcn copy-paste (Button, Card, Dialog, ...)
│   │   ├── layout/              # AppShell, Sidebar, TopBar
│   │   ├── feedback/            # Toast, EmptyState, ErrorBoundary
│   │   ├── data/                # DataTable, Pagination, Filters
│   │   └── forms/               # FormField, FormSection (RHF wrappers)
│   ├── features/                # vertical slices por dominio
│   │   ├── auth/                # T-02, T-03, T-04b
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   └── api.ts
│   │   ├── projects/            # T-04
│   │   ├── wizard/              # T-10.1 a T-10.5 (epico — ver secao L)
│   │   ├── pro-editor/          # T-20 (desktop-first)
│   │   ├── report/              # T-30 + drill-down
│   │   ├── account/             # T-40
│   │   ├── workspace/           # T-50
│   │   └── api-keys/            # T-60
│   ├── hooks/                   # hooks reutilizaveis (useDebounce, useMediaQuery, ...)
│   ├── lib/                     # utilitarios puros (sem React)
│   │   ├── format.ts            # numero/unidade (kN, m², ...)
│   │   ├── cep.ts               # validacao + mascara CEP
│   │   ├── nbr-citation.ts      # formata "NBR 6118:2014 §17.2"
│   │   └── zod-helpers.ts
│   ├── routes/                  # arvore de rotas
│   │   ├── __root.tsx
│   │   ├── index.tsx            # T-01 landing
│   │   ├── login.tsx            # T-03
│   │   ├── signup.tsx           # T-02
│   │   ├── recover.tsx          # T-04b
│   │   ├── _authed/             # layout autenticado (guard)
│   │   │   ├── projects/
│   │   │   │   ├── index.tsx    # T-04
│   │   │   │   ├── new-wizard.tsx
│   │   │   │   ├── new-pro.tsx
│   │   │   │   └── $projectId/
│   │   │   │       ├── report.tsx   # T-30
│   │   │   │       └── editor.tsx   # T-20
│   │   │   ├── account.tsx      # T-40
│   │   │   ├── workspace.tsx    # T-50
│   │   │   └── api-keys.tsx     # T-60
│   ├── store/                   # Zustand stores (UI state apenas)
│   │   ├── ui.ts                # sidebar collapsed, theme
│   │   └── wizard.ts            # estado do wizard 5 passos
│   ├── styles/
│   │   ├── globals.css          # tailwind base + CSS vars (tokens)
│   │   └── tokens.css           # cores, spacing, typography
│   ├── locales/                 # i18n
│   │   ├── pt-BR/
│   │   │   ├── common.json
│   │   │   ├── wizard.json
│   │   │   └── report.json
│   │   └── en-US/               # v2 (ver secao H)
│   ├── test/
│   │   ├── setup.ts             # vitest + RTL setup
│   │   ├── msw/                 # mocks de API
│   │   └── utils.tsx            # render helpers
│   ├── App.tsx
│   ├── main.tsx
│   └── env.d.ts
├── e2e/                         # Playwright (S0-T17)
│   ├── fixtures/
│   └── specs/
├── .env.example
├── .eslintrc.cjs
├── .prettierrc
├── index.html
├── package.json
├── playwright.config.ts
├── postcss.config.js
├── tailwind.config.ts
├── tsconfig.json
├── vite.config.ts
└── vitest.config.ts
```

Total: 30+ entradas relevantes. Convencao: `features/` sao verticais (cada feature dona dos seus components/hooks/api), `components/` sao horizontais reutilizaveis.

---

## C. Camadas

### 1. API client

- **Geracao:** `openapi-typescript-codegen` consome `docs/api/openapi.yaml` (publicado em S1-T11) e emite types + services em `src/api/generated/`.
- **Script:** `pnpm api:codegen` → `openapi --input ../../docs/api/openapi.yaml --output src/api/generated --client axios --useOptions`.
- **Wrapper:** `src/api/client.ts` adiciona interceptors (auth, refresh, error mapping). Codigo de feature **nunca** importa de `generated/` direto — sempre via hook em `features/*/api.ts`.
- **DoD:** alteracao de schema Pydantic no backend → `pnpm api:codegen` no front quebra build se contrato mudou. Type safety end-to-end honra RNF-5.2/5.3.

### 2. State

| Tipo | Lib | Justificativa |
|---|---|---|
| Server state | TanStack Query v5 | Padrao de mercado, cache automatico, devtools excelentes. Cobre 90% do que o app precisa. |
| UI state local | **Zustand** | 1.5KB gz, sem boilerplate, sem context hell. Usado pra: sidebar collapsed, tema, estado do wizard 5 passos (multi-step). |
| Form state | React Hook Form | Ver secao 4. |

**Por que NAO Redux/RTK:** Redux Toolkit traz reducers, slices, middlewares e codegen pesado. Pro escopo (CRUD + wizard + tabelas), TanStack Query + Zustand cobrem o caso com 1/10 do codigo. Redux faz sentido em apps com **state global cliente** complexo (offline-first, optimistic deep), nao e o nosso caso — quase tudo e server state.

### 3. Routing

**Recomendacao: TanStack Router.**

| Criterio | TanStack Router | React Router v6 |
|---|---|---|
| Type-safe routes | ✅ nativo | ⚠ via plugin terceiro |
| Search params tipados | ✅ | ❌ |
| Loaders + cache integration | ✅ pareia com TanStack Query | ⚠ separado |
| Maturidade | v1 estavel desde 2024 | v6 estavel ha anos |
| Bundle | ~14KB | ~10KB |

Como ja usamos TanStack Query e o app tem rotas dinamicas com filtros (`/projects?status=draft&page=2`), **TanStack Router** elimina classes inteiras de bug (search params digitados a string). Decisao final em War Room (secao N).

### 4. Forms

- **Lib:** React Hook Form + Zod (resolver `@hookform/resolvers/zod`).
- **Espelho do backend:** schemas Zod em `features/*/schemas.ts` espelham os Pydantic (RF-3, RF-4). Em CI, um script confere que os campos batem (`pnpm schema:check`).
- **Pattern:** wrapper `<FormField name="..." label="..." />` em `components/forms/` — feature so define schema e renderiza, nada de `register` cru.
- **Aplicado em:** wizard (T-10), editor PRO (T-20), config de conta (T-40), workspace (T-50).

### 5. Design system

- **Base:** shadcn/ui (Radix + Tailwind), componentes copia-cola em `src/components/ui/`. Versao travada por commit, nao por npm.
- **Tokens** em `src/styles/tokens.css` via CSS vars:
  - Cores: `--color-bg`, `--color-fg`, `--color-primary`, `--color-success`, `--color-warning`, `--color-danger` (mapeia status de T-30: `✓` aprovado, `⚠` flecha excedida).
  - Spacing: escala 4px (0, 1, 2, 4, 6, 8, 12, 16, 24, 32...).
  - Typography: `--font-sans` (Inter), `--font-mono` (JetBrains Mono pra tabelas numericas em T-20/T-30).
  - Radius, shadow, z-index idem.
- **Tema claro + escuro** via classe `.dark` no `<html>`. Persistido em `localStorage` + `prefers-color-scheme` no primeiro load.
- **Densidade:** `compact` mode em tabelas do editor PRO (T-20) — densidade maior por preferencia de engenheiros estruturais.

---

## D. Telas (mapping pra `06-FLUXOS-DE-TELA.md`)

| Tela | Nome | Localizacao | Complexidade | Sprint | Dependencia API |
|---|---|---|---|---|---|
| T-01 | Landing publica | `routes/index.tsx` | pequeno | S0 (S0-T16) | — |
| T-02 | Signup | `routes/signup.tsx` + `features/auth/` | pequeno | S0 (S0-T16) | RF-1.1 (S0-T10) |
| T-03 | Login | `routes/login.tsx` + `features/auth/` | pequeno | S0 (S0-T16) | RF-1.1 (S0-T10) |
| T-04b | Recuperar senha | `routes/recover.tsx` | pequeno | S1 | RF-1.2 |
| T-04 | Dashboard projetos | `routes/_authed/projects/index.tsx` + `features/projects/` | medio | S1 (S1-T08) | RF-2.1 (S1-T03) |
| T-10 | Wizard 5 passos | `features/wizard/` (subpastas por step) | **epico** | S5 | RF-3.* + RF-7.2/7.3 + RF-6.* |
| T-15 | Cale em andamento | `features/wizard/components/CalcProgress.tsx` | pequeno | S5 | RNF-6.2 (Celery + WS/polling) |
| T-20 | Editor PRO | `features/pro-editor/` | **epico** | S11 | RF-4.* |
| T-30 | Relatorio + drill-down | `features/report/` | grande | S3 | RF-8.* + RF-10.3 |
| T-40 | Config de conta | `routes/_authed/account.tsx` | pequeno | S1 (S1-T09) | RF-1 |
| T-50 | Workspace | `routes/_authed/workspace.tsx` + `features/workspace/` | medio | S21 | RF-1.4, RF-1.5 |
| T-60 | API keys | `routes/_authed/api-keys.tsx` + `features/api-keys/` | pequeno | S13+ | RF-9.2 |
| T-erro | Erro de norma | `features/report/components/CalcError.tsx` | pequeno | S6 | RF-8.1 (mensagem 422) |
| T-erro | Cota free | `components/feedback/QuotaModal.tsx` | pequeno | S13 | billing |

Sprints sao alinhadas a `08-SPRINTS.md`. As que nao tem task FE explicita la entram via secao **L** abaixo.

---

## E. Mobile + responsividade

- **Breakpoints (Tailwind):** `sm` 640 · `md` 768 · `lg` 1024 · `xl` 1280 · `2xl` 1536.
- **Mobile-first ate T-30** (alinhado com `06-FLUXOS-DE-TELA.md` Principio 5): T-01, T-02, T-03, T-04, T-10 (wizard), T-15, T-30 (relatorio).
- **Editor PRO (T-20) e desktop-first**: ao detectar `< lg`, renderiza tela de aviso "Editor PRO requer tela maior. Use o Wizard ou abra em desktop." com link pra abrir em modo somente-leitura.
- **Tabelas de resultado (T-30):** em mobile vira stack de cards (uma linha = um card), em desktop vira tabela densa.
- **Aceitacao:** "Mobile: dashboard + relatorio legiveis em 360px" (criterio de UX em `06-FLUXOS-DE-TELA.md`).

---

## F. Acessibilidade

- **Target:** WCAG 2.1 AA.
- **Como:**
  - Radix primitives (base do shadcn/ui) ja cobrem foco, ARIA, keyboard nav.
  - Foco visivel (`focus-visible:ring-2`) em todos componentes interativos.
  - Contraste minimo 4.5:1 — token `--color-fg` sobre `--color-bg` validado em ambos temas.
  - Semantic HTML (`<nav>`, `<main>`, `<section>`, `<button>` sempre que clicavel).
  - `aria-label` obrigatorio em icon-only buttons.
  - Skip-link "pular pra conteudo" no AppShell.
- **CI:** `@axe-core/playwright` nas specs E2E criticas (login, dashboard, wizard step 1, relatorio). Regressao de a11y bloqueia PR.

---

## G. Performance

- **Targets:**
  - Lighthouse Performance > 90 nas paginas publicas (T-01) e T-04.
  - Lighthouse Accessibility > 90 em todas.
  - LCP < 2.5s em 4G simulado.
- **Tecnicas:**
  - Code-split por rota (TanStack Router faz nativo).
  - Bundle budget **< 250KB gzip por chunk** (rollup-plugin-visualizer no CI).
  - Lazy-load do editor PRO (T-20) — pesa ~150KB sozinho, so carrega quando o usuario entra.
  - Imagens em `/public` em WebP/AVIF, com `loading="lazy"`.
  - Fonts via `font-display: swap` + preload do peso 400 + 600.
  - TanStack Query: `staleTime` agressivo em listas (1 min), refetch on focus desligado em mobile.

---

## H. Internacionalizacao

- **Lib:** `react-i18next` (recomendado sobre Lingui — ecossistema maior, plurals + ICU MessageFormat ok, dev tools melhores).
- **Locales (v1):** `pt-BR` only.
- **Locales (v2):** `en-US`. Strings extraidas do codigo desde o dia 1 — `t('wizard.step1.title')` em vez de string crua.
- **Estrutura:** `src/locales/<locale>/<namespace>.json` (namespaces: `common`, `auth`, `wizard`, `report`, `editor`, `errors`).
- **Numero/unidade:** wrapper `formatKN(value)`, `formatM2(value)` em `src/lib/format.ts` usa `Intl.NumberFormat` com locale ativo (PT-BR usa virgula decimal).
- **Citacoes de norma:** sempre em PT-BR no MVP (NBR e em portugues). Quando v2 entrar EN-US, manter citacao NBR no idioma original (norma e fonte juridica) e traduzir so o texto explicativo.

---

## I. Auth flow

- **Backend:** FastAPI Users + JWT access+refresh (`03-DESIGN.md` stack).
- **Storage:** access token em memoria (Zustand store nao persistido); refresh token em cookie `httpOnly` `Secure` `SameSite=Lax` (mitiga XSS — RNF-3.3).
- **Interceptor:** `src/api/client.ts`:
  - Anexa `Authorization: Bearer <access>` em toda request.
  - Em 401, tenta refresh (1x) → reenvia request original.
  - Em 401 do proprio refresh → limpa cache TanStack (`queryClient.clear()`) + redirect `/login?next=<path>`.
- **Logout:** chama `/auth/logout` (revoga refresh server-side) + `queryClient.clear()` + redirect `/`.
- **Guard de rota:** layout `_authed/` em TanStack Router faz `beforeLoad` checando access valido; sem token redireciona pra `/login`.

---

## J. Erros

- **Boundary global:** `<ErrorBoundary>` no root captura render errors → fallback "Algo deu errado, equipe avisada" + Sentry React (`@sentry/react`).
- **Mapping de erros HTTP** (em `src/api/errors.ts`):
  - **401** → trigger refresh + retry; se falhar, redirect login.
  - **403** → toast "Sem permissao" + log estruturado.
  - **422** (validation Pydantic) → mostra erros nos campos do form (RHF `setError` por campo, mapeando `loc`).
  - **422 em calculo de norma** → componente `<CalcErrorCard />` (referencia `06-FLUXOS-DE-TELA.md` "Calculo falhou (norma rejeitou)"): titulo "Nao foi possivel dimensionar", lista de violacoes, sugestao acionavel ("aumentar secao pra 20×30 ou reduzir altura"), botoes contextuais ("Editar pilar P3", "Ver outros problemas"). Layout segue exatamente o wireframe la.
  - **5xx** → toast "Erro interno, tente novamente" + Sentry com `event_id` e botao "Reportar".
- **Cota atingida (Free):** modal `<QuotaModal />` espelhando wireframe "Cota free atingida" em `06-FLUXOS-DE-TELA.md`. Trigger via response `429` ou flag `quota_exceeded` em `/me`.

---

## K. Testes

| Camada | Lib | Escopo | Target |
|---|---|---|---|
| Unit | **Vitest** | `lib/`, `hooks/`, helpers puros | > 90% |
| Componente | **React Testing Library** + Vitest + MSW (mock API) | `components/` e `features/*/components/` | > 70% |
| E2E | **Playwright** (ja em S0-T17) | jornadas criticas: signup → wizard → calculo → relatorio | smoke + happy path por sprint |
| Acessibilidade | `@axe-core/playwright` | mesmas specs E2E | zero violations criticas |
| Visual | Playwright screenshots (opcional) | T-04, T-10.5, T-30 | snapshot diff |

- **Coverage gate** no CI: `> 70%` em `features/`, `> 90%` em `lib/`. Falha => PR bloqueado.
- **MSW** (`src/test/msw/`) serve handlers que espelham o OpenAPI gerado — fonte da verdade unica.

---

## L. Sprints especificas (proposta de atualizacao a `08-SPRINTS.md`)

`08-SPRINTS.md` ja tem **S0-T16**, **S0-T17**, **S1-T08**, **S1-T09**. As tasks abaixo cobrem o restante do front que falta no plano. **Owner padrao: Iris** (FE), salvo nota.

### S0 — Limpeza e fundacao (ja parcial)
- **S0-T16** (existente) — setup Vite + React + TS + shadcn/ui + TanStack Query, landing + signup/login.
- **S0-T19** (novo) — i18n base (`react-i18next` + `pt-BR/common.json`) + tema claro/escuro + tokens CSS vars. Estim: medio.
- **S0-T20** (novo) — bundle budget no CI + Lighthouse CI no PR. Estim: pequeno.

### S1 — Dominio + persistencia
- **S1-T08** (existente) — Dashboard projetos (T-04).
- **S1-T09** (existente) — Tela de configuracoes de conta (T-40).
- **S1-T13** (novo) — Tela de auth completa: signup com confirmacao email, recuperar senha (T-04b), email de confirmacao. Estim: medio.
- **S1-T14** (novo) — Setup `openapi-typescript-codegen` integrado a `S1-T11` (OpenAPI export). Estim: pequeno.

### S3 — Pos motor de calculo
- **S3-Tfe1** (novo) — Tela de relatorio T-30 (resumo + tabela de verificacoes). Estim: grande.
- **S3-Tfe2** (novo) — Drill-down de elemento T-30 (esforcos, armadura, citacoes NBR). Estim: medio.
- **S3-Tfe3** (novo) — Export PDF/JSON botoes integrados ao `report` service do backend. Estim: medio.

### S5 — Wizard leigo (epico)
- **S5-Tfe1** (novo) — Wizard infra: `features/wizard/`, store Zustand multi-step, validacao por step. Estim: grande.
- **S5-Tfe2** (novo) — Steps T-10.1 (tipo de obra) + T-10.2 (geometria com preview 2D simples canvas/svg). Estim: grande.
- **S5-Tfe3** (novo) — Step T-10.3 (CEP → vento + sismo, com preview ajustavel). Estim: medio.
- **S5-Tfe4** (novo) — Step T-10.4 (sondagem SPT por camada OU premissa conservadora). Estim: medio.
- **S5-Tfe5** (novo) — Step T-10.5 (resumo + calcular) + tela T-15 (progresso live via WS ou polling). Estim: medio.
- **S5-Tfe6** (novo, **obrigatorio**) — **Teste de UX com 3 usuarios reais** (criterio em `06-FLUXOS-DE-TELA.md` "Wizard leigo concluido em < 10 min"). Owner: Iris + Ayla. Estim: medio. Sem este, sprint nao fecha.

### S6 — Versoes + estados de erro
- **S6-Tfe1** (novo) — Tela de versoes do projeto (T-30 sidebar "Historico"). Estim: medio.
- **S6-Tfe2** (novo) — Componentes `<CalcErrorCard />` + `<QuotaModal />` (referencia secao J). Estim: pequeno.

### S11 — Editor PRO (epico, desktop-first)
- **S11-Tfe1** — Layout 3 colunas (arvore | central | propriedades) ja com guards mobile. Estim: grande.
- **S11-Tfe2** — Abas Nos / Barras / Cargas / Combinacoes (tabelas editaveis). Estim: epico.
- **S11-Tfe3** — Painel de propriedades + override de coeficientes com justificativa obrigatoria (RF-4.4). Estim: grande.
- **S11-Tfe4** — Esquema 2D do modelo (svg, sem 3D). Estim: medio.

### S13 — Billing
- **S13-Tfe1** — Stripe Checkout integration (botoes "Upgrade" em T-04 e em `<QuotaModal />`). Estim: medio.
- **S13-Tfe2** — Tela de plano/faturas em T-40. Estim: medio.

### S21 — Workspace multi-usuario
- **S21-Tfe1** — Tela T-50 (membros + convites + RBAC). Estim: grande.
- **S21-Tfe2** — Trocador de workspace no AppShell. Estim: pequeno.

> Numeracao definitiva (S3-Tfe1 etc.) sera reconciliada quando estas tasks entrarem em `08-SPRINTS.md`. Forma proposta: **Hera** abre PR atualizando o doc.

---

## M. Integracao CI/CD

- **Manager:** pnpm 9 (workspace `apps/web`).
- **Pipeline (GitHub Actions, em `.github/workflows/web.yml`):**
  - `pnpm install --frozen-lockfile`
  - `pnpm typecheck` (tsc --noEmit)
  - `pnpm lint` (eslint + prettier check)
  - `pnpm test` (vitest run + coverage)
  - `pnpm build` (vite build, bundle budget enforce)
  - `pnpm test:e2e` (playwright em headed:false, contra preview deploy)
  - `pnpm lighthouse` (Lighthouse CI gate >= 90 perf + a11y)
- **Preview deploys por PR:** comentario automatico com URL. Plataforma — decisao em **N**.
- **Promote:** merge em `main` → deploy producao.

---

## N. Decisoes abertas (vao pra War Room)

1. **shadcn/ui vs Mantine vs Chakra UI** — recomendacao deste doc e shadcn/ui (Radix + Tailwind, copy-paste, sem lock-in). Mantine e mais "bateria inclusa" mas trava em versoes; Chakra esta em transicao v3.
2. **TanStack Router vs React Router v6** — recomendacao deste doc e TanStack Router (search params tipados + integracao TanStack Query). Custo: lib mais nova, time precisa estudar.
3. **Vercel vs Cloudflare Pages vs Fly.io** pra hosting do front — `03-DESIGN.md` cita Fly.io/Railway pro backend; consistencia favorece Fly.io tambem pro front estatico. Cloudflare Pages e barato e tem CDN global. Vercel tem melhor DX mas custa mais.
4. **Headless CMS pra landing (T-01)?** — opcoes: Sanity, Contentful, Strapi self-hosted, ou simplesmente MDX no proprio repo. Decisao depende de quem vai editar copy (engenharia vs marketing futuro).
