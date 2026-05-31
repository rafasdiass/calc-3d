---
documento: fluxos de tela e wireframes textuais
versao: 1.0
data: 2026-05-31
escopo: MVP (Fase 1 + Fase 2) — telas marcadas [F1] [F2]
---

# 06 — FLUXOS DE TELA E WIREFRAMES TEXTUAIS

## Mapa de telas (alto nível)

```
ANÔNIMO                                       LOGADO
───────                                       ──────
[T-01] Landing public  ──login───────────►  [T-04] Dashboard projetos
[T-02] Signup                                       │
[T-03] Login                                        ├──► [T-10] Wizard leigo (5 passos)
[T-04b] Recuperar senha                             ├──► [T-20] Editor PRO (paramétrico)
                                                    ├──► [T-30] Relatório / resultado
                                                    ├──► [T-40] Configurações de conta
                                                    ├──► [T-50] Workspace (Studio)
                                                    └──► [T-60] API keys & docs
```

## Princípios de UX

1. **Cada tela tem 1 ação primária**. Botões secundários sempre menores e textuais.
2. **Wizard leigo nunca pede o que pode inferir**. Se faltou input, mostra default + botão "ajustar".
3. **PRO sempre tem o "leigo" como ponto de partida**. Pode pular o wizard, mas não há tela "Pro virgem".
4. **Cada cálculo mostra norma e fórmula em hover/expand**. Citação inline obrigatória.
5. **Mobile-friendly até T-30**. Editor PRO (T-20) é desktop-first.

---

## [T-01] Landing pública

```
┌──────────────────────────────────────────────────────────────────┐
│ calc-engine                                  [Login]  [Criar conta]│
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│   Cálculo estrutural normativo.                                   │
│   Em minutos. Não em meses.                                       │
│                                                                    │
│   [ Começar grátis →  ]    Ver exemplo                            │
│                                                                    │
│  ────────────────────────────────────────                         │
│                                                                    │
│  ✓ NBR + Eurocode + ACI nativos                                   │
│  ✓ Solo + estrutura no mesmo motor                                │
│  ✓ Wizard pra leigo · Editor pro pro engenheiro                   │
│  ✓ Sem instalação. Web. Mobile. Onde estiver.                     │
│                                                                    │
└──────────────────────────────────────────────────────────────────┘
```

**Ações**: `Criar conta` → T-02 · `Login` → T-03 · `Ver exemplo` → projeto demo somente leitura

---

## [T-02] Signup [F0]

```
┌──────────────────────────────────────────────┐
│ Criar conta                                  │
├──────────────────────────────────────────────┤
│ Email           [_______________________]    │
│ Senha           [_______________________]    │
│ Tipo de uso     ( ) Estudante                │
│                 ( ) Engenheiro autônomo      │
│                 ( ) Escritório               │
│ □ Aceito termos                              │
│                                              │
│        [   Criar conta  ]                    │
│                                              │
│ Já tem conta? Entrar                         │
└──────────────────────────────────────────────┘
```

**Validação**: email único, senha forte (8+, número, símbolo). Email de confirmação obrigatório antes de T-04.

---

## [T-04] Dashboard de projetos [F0/F1]

```
┌─────────────────────────────────────────────────────────────────┐
│ calc-engine        [Projetos] [Configurações]    rafa@x  [Sair] │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Meus projetos                              [+ Novo projeto ▼]   │
│                                              ├ Wizard simples   │
│                                              └ Editor PRO       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Casa do João           Residencial · 80m²  · 1 pav         │ │
│  │ Atualizado há 2h       NBR 6118 · NBR 6122 · NBR 6123      │ │
│  │ Status: ✓ Calculado                       [Ver] [Duplicar] │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Galpão Itu             Industrial · 1200m² · 1 pav         │ │
│  │ Em rascunho                                  [Continuar]   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Plano: Free · 1/3 projetos este mês     [Upgrade]               │
└─────────────────────────────────────────────────────────────────┘
```

---

## [T-10] Wizard leigo — 5 passos [F1] ⭐ tela mais importante do MVP

### T-10.1 — Tipo de obra
```
┌─────────────────────────────────────────────────────────────────┐
│ Novo projeto · 1 de 5                              [Cancelar]   │
│ ●───────○───────○───────○───────○                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Que tipo de obra você está calculando?                          │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                │
│  │  🏠         │ │  🏢         │ │  🏭         │                │
│  │ Residência  │ │ Comercial   │ │ Galpão      │                │
│  │ uni/multi   │ │             │ │ industrial  │                │
│  └─────────────┘ └─────────────┘ └─────────────┘                │
│  ┌─────────────┐ ┌─────────────┐                                │
│  │  🛡️         │ │  🚪         │                                │
│  │ Muro de     │ │ Outro       │                                │
│  │ arrimo      │ │             │                                │
│  └─────────────┘ └─────────────┘                                │
│                                                                  │
│                                  [< Voltar]    [Próximo >]       │
└─────────────────────────────────────────────────────────────────┘
```

### T-10.2 — Geometria simplificada
```
┌─────────────────────────────────────────────────────────────────┐
│ Novo projeto · 2 de 5                                            │
│ ●───────●───────○───────○───────○                                │
├─────────────────────────────────────────────────────────────────┤
│  Geometria básica                                                │
│                                                                  │
│  Pavimentos          [1] (térreo + N pavimentos)                 │
│  Pé-direito          [2.80] m                                    │
│                                                                  │
│  Planta retangular                                               │
│  Largura X           [10.00] m                                   │
│  Largura Y           [8.00 ] m                                   │
│                                                                  │
│  Grid de pilares                                                 │
│  Vãos em X           [auto] ▼  ← inferido por NBR 6118 (vão econ.)│
│  Vãos em Y           [auto] ▼                                    │
│                                                                  │
│  ┌─────────────────────────────┐                                 │
│  │   ○────○────○────○          │  ← preview 2D (planta)          │
│  │   │    │    │    │          │                                 │
│  │   ○────○────○────○          │                                 │
│  │   │    │    │    │          │                                 │
│  │   ○────○────○────○          │                                 │
│  └─────────────────────────────┘                                 │
│                                                                  │
│                                  [< Voltar]    [Próximo >]       │
└─────────────────────────────────────────────────────────────────┘
```

### T-10.3 — Local da obra (alimenta vento + sismo)
```
┌─────────────────────────────────────────────────────────────────┐
│ Novo projeto · 3 de 5                                            │
│ ●───────●───────●───────○───────○                                │
├─────────────────────────────────────────────────────────────────┤
│  Local da obra                                                   │
│                                                                  │
│  CEP                 [01310-100]   [Buscar]                      │
│                                                                  │
│  Endereço inferido   Av. Paulista, São Paulo, SP                 │
│                                                                  │
│  Vento                                                           │
│  Velocidade básica V₀ = 40 m/s     ← NBR 6123 mapa isopletas    │
│  Categoria de terreno  [IV - cidade] ▼                           │
│  Topografia            [plana]       ▼                           │
│                                                                  │
│  Sismo (NBR 15421)   Zona 0 (não há ação sísmica)               │
│                                                                  │
│  [✏ Ajustar manualmente]                                         │
│                                                                  │
│                                  [< Voltar]    [Próximo >]       │
└─────────────────────────────────────────────────────────────────┘
```

### T-10.4 — Sondagem (SPT)
```
┌─────────────────────────────────────────────────────────────────┐
│ Novo projeto · 4 de 5                                            │
│ ●───────●───────●───────●───────○                                │
├─────────────────────────────────────────────────────────────────┤
│  Sondagem do solo                                                │
│                                                                  │
│  ( ) Tenho relatório SPT  → input simplificado por camada        │
│  (●) Não tenho sondagem   → premissa conservadora explícita      │
│                                                                  │
│  ─ se "tenho SPT" ─                                             │
│  Profundidade   N(SPT)   Tipo de solo                            │
│  0 - 2 m        [4]      [Argila mole]    ▼   [×]                │
│  2 - 5 m        [12]     [Areia média]    ▼   [×]                │
│  5 - 10 m       [25]     [Areia compacta] ▼   [×]                │
│  [+ adicionar camada]                                            │
│  Nível d'água [3.0] m                                            │
│                                                                  │
│  ─ se "não tenho" ─                                             │
│  ⚠ Vamos usar premissa: argila média uniforme (q_adm = 100 kPa) │
│  Você precisará confirmar com sondagem antes da execução real.  │
│  □ Entendi a limitação                                           │
│                                                                  │
│                                  [< Voltar]    [Próximo >]       │
└─────────────────────────────────────────────────────────────────┘
```

### T-10.5 — Confirmação e cálculo
```
┌─────────────────────────────────────────────────────────────────┐
│ Novo projeto · 5 de 5                                            │
│ ●───────●───────●───────●───────●                                │
├─────────────────────────────────────────────────────────────────┤
│  Resumo · pronto pra calcular                                    │
│                                                                  │
│  Obra      Casa do João · residencial 1 pav · 80m²              │
│  Local     SP, vento V₀=40 m/s, sismo zona 0                     │
│  Solo      3 camadas SPT, NA=3m                                  │
│  Material  Concreto C25 (default), aço CA-50                     │
│  Normas    NBR 6118:2014, 6120:2019, 6122:2022, 6123:1988,       │
│            8681:2003                                              │
│                                                                  │
│  Defaults aplicados (clique pra ajustar):                        │
│  • Carga acidental: 1,5 kN/m² (residencial NBR 6120)        ✏  │
│  • Combinações: padrão NBR 8681                              ✏  │
│  • Coeficientes γc=1,4 / γs=1,15                             ✏  │
│                                                                  │
│  Tempo estimado de cálculo: ~25s                                │
│                                                                  │
│                       [< Voltar]    [▶ CALCULAR AGORA]           │
└─────────────────────────────────────────────────────────────────┘
```

---

## [T-15] Tela de cálculo em andamento

```
┌─────────────────────────────────────────────────────────────────┐
│  Calculando "Casa do João"...                                    │
│                                                                  │
│  ▰▰▰▰▰▰▰▰▰▰▰▱▱▱▱  72%                                            │
│                                                                  │
│  ✓ Modelo gerado (12 nós, 17 barras)                             │
│  ✓ Cargas aplicadas (PP + 1,5 kN/m² + vento)                     │
│  ✓ FEM resolvido                                                 │
│  ✓ Dimensionamento concreto NBR 6118                             │
│  ⟳ Verificação geotécnica NBR 6122...                            │
│  ○ Geração de relatório                                          │
│                                                                  │
│  Você pode fechar — vamos te avisar.                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## [T-30] Relatório / Resultado [F1]

```
┌────────────────────────────────────────────────────────────────────┐
│ Casa do João · Calculado · v1                  [PDF] [JSON] [DXF]  │
├──────────────────┬─────────────────────────────────────────────────┤
│ Resumo           │  ┌─────────────────────────────────────────────┐│
│  Visão geral     │  │  ✓ Estrutura aprovada                       ││
│  Materiais       │  │  Volume concreto:    8,4 m³                 ││
│                  │  │  Peso aço:         412 kg                   ││
│ Verificações     │  │  Área fôrma:       142 m²                   ││
│  ✓ Vigas (5)     │  └─────────────────────────────────────────────┘│
│  ✓ Pilares (8)   │                                                  │
│  ⚠ Lajes (3)     │  Verificação por elemento ▼                     │
│  ✓ Sapatas (4)   │  ┌──────┬─────────┬──────┬──────────┬─────────┐│
│                  │  │ ID   │ Tipo    │ Util │ Norma    │ Status  ││
│ Memória cálc.    │  ├──────┼─────────┼──────┼──────────┼─────────┤│
│  PDF completo    │  │ V1   │ Viga    │ 78%  │ NBR 6118 │ ✓       ││
│                  │  │ V2   │ Viga    │ 65%  │ NBR 6118 │ ✓       ││
│ Histórico        │  │ P1   │ Pilar   │ 88%  │ NBR 6118 │ ✓       ││
│  v1 · agora      │  │ L2   │ Laje    │103%  │ NBR 6118 │ ⚠ flecha││
│                  │  │ S1   │ Sapata  │ 72%  │ NBR 6122 │ ✓       ││
│                  │  └──────┴─────────┴──────┴──────────┴─────────┘│
│                  │  Clique numa linha pra ver detalhe + memória.   │
│                  │                                                  │
│                  │  [Recalcular com ajustes]  [Compartilhar]       │
└──────────────────┴─────────────────────────────────────────────────┘
```

### T-30 detalhe de elemento (drill-down)

```
┌────────────────────────────────────────────────────────────────────┐
│ ← Voltar     V1 · Viga 20×40 · L=4,5m                              │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Esforços (envoltória ELU)                                         │
│  Md (apoio)        38,2 kN·m                                       │
│  Md (vão)          24,1 kN·m                                       │
│  Vd                42,7 kN                                         │
│                                                                    │
│  Armadura calculada                                                │
│  Apoio:  As = 4,12 cm² → 3 ø 12,5 mm  (NBR 6118 §17.3.5)          │
│  Vão:    As = 2,68 cm² → 3 ø 10,0 mm                               │
│  Cisalh: estribo ø6,3 c/15 cm                                      │
│                                                                    │
│  Verificações                                                      │
│  ✓ ELU flexão (η = 78%)        NBR 6118:2014 §17.2                │
│  ✓ ELU cisalhamento (η = 64%)  NBR 6118:2014 §17.4                │
│  ✓ ELS-DEF flecha (12mm/833)   NBR 6118:2014 §17.3.2              │
│  ✓ ELS-W fissuração (wk<0.3mm) NBR 6118:2014 §17.3.3              │
│                                                                    │
│  [Ver memória de cálculo passo-a-passo ▼]                          │
└────────────────────────────────────────────────────────────────────┘
```

---

## [T-20] Editor PRO (paramétrico) [F2]

```
┌─────────────────────────────────────────────────────────────────────┐
│ Casa do João  ·  PRO mode                       [Calcular] [Sair PRO]│
├─────────┬───────────────────────────────────────┬─────────────────────┤
│ Árvore  │  Editor central                       │ Propriedades       │
│         │                                       │ (do selecionado)   │
│ ▼ Geom  │  Aba: [Nós] [Barras] [Cargas] [Comb]  │                    │
│  Nós (12)│ ┌────┬──────┬──────┬──────┐          │ Barra B5           │
│  Barras │  │ ID │ X(m) │ Y(m) │ Z(m) │          │ Tipo: viga         │
│  (17)   │  ├────┼──────┼──────┼──────┤          │ Material: C25      │
│         │  │ N1 │ 0    │ 0    │ 0    │          │ Seção: 20×40 cm    │
│ ▼ Mat   │  │ N2 │ 5    │ 0    │ 0    │          │ Nós: N4 → N5       │
│  C25    │  │ N3 │ 5    │ 4    │ 0    │          │                    │
│  C30    │  │ ... │     │      │      │          │ Coeficientes       │
│  CA-50  │  └────┴──────┴──────┴──────┘          │ γc = 1.4   [✏]    │
│         │                                       │ γs = 1.15  [✏]    │
│ ▼ Cargas│                                       │ γf = 1.4   [✏]    │
│  CP+CV  │  Esquema 2D do modelo (sem 3D):       │                    │
│  Vento  │  ┌─────────────────────────────────┐  │ Justificativa de   │
│         │  │  ●─────●─────●  ← V (linha)     │  │ override:          │
│ ▼ Norma │  │  │     │     │                  │  │ [_____________]    │
│  NBR 6118│ │  ●─────●─────●  ← P (símbolo △) │  │                    │
│  NBR 8681│ │                                  │  │ [Reset default]    │
│         │  └─────────────────────────────────┘  │                    │
└─────────┴───────────────────────────────────────┴─────────────────────┘
```

---

## [T-50] Workspace / Multi-usuário (tier Studio) [F3]

```
┌─────────────────────────────────────────────────────────────────┐
│ Workspace: Engenharia Silva & Cia                               │
├─────────────────────────────────────────────────────────────────┤
│  Membros (4)                                  [+ Convidar]      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Carlos Silva    Owner       carlos@x          [⚙]       │   │
│  │ Ana Pereira     Editor      ana@x             [⚙] [×]   │   │
│  │ João Souza      Editor      joao@x            [⚙] [×]   │   │
│  │ Maria Costa     Viewer      maria@x           [⚙] [×]   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Projetos compartilhados (12)            [Listar todos →]       │
│  Plano: Studio · 4/10 usuários · R$ XXX/mês                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## [T-60] API keys e docs (tier Pro+) [F2/F3]

```
┌─────────────────────────────────────────────────────────────────┐
│ API · keys e documentação                                        │
├─────────────────────────────────────────────────────────────────┤
│  Suas chaves                                  [+ Nova chave]    │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ Default · ck_live_abc123...     Criada 2026-05-31  [×] │    │
│  │ Escopo: read+write · 600 req/min                       │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Documentação                                                   │
│  📖 OpenAPI / Swagger                                           │
│  📖 Guia de início rápido                                       │
│  📖 Exemplos: Python, cURL, Grasshopper                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Estados de erro

### Cálculo falhou (norma rejeitou)
```
┌──────────────────────────────────────────────────────┐
│ ⚠ Não foi possível dimensionar                       │
│                                                      │
│ Pilar P3: ρ = 0,42% < ρmín = 0,40%  → ok             │
│ Pilar P3: λ = 95 > λlim = 90 (NBR 6118 §15.8.2)      │
│   → Esbeltez excessiva. Sugestão: aumentar seção     │
│     pra 20×30 ou reduzir altura.                     │
│                                                      │
│ [Editar pilar P3]   [Ver outros problemas]           │
└──────────────────────────────────────────────────────┘
```

### Cota free atingida
```
┌──────────────────────────────────────────────────────┐
│ Plano Free: 3/3 projetos este mês                    │
│                                                      │
│ Pra criar novos projetos, faça upgrade.              │
│                                                      │
│ [Ver planos]                       [Fechar]          │
└──────────────────────────────────────────────────────┘
```

---

## Telas adicionadas (correcao WR-001)

### [T-03] Login [F0]
```
┌──────────────────────────────────────────────┐
│ Login                                        │
├──────────────────────────────────────────────┤
│ Email           [_______________________]    │
│ Senha           [_______________________]    │
│ □ Lembrar-me                                 │
│                                              │
│        [   Entrar  ]                         │
│                                              │
│ Esqueci a senha   ·   Criar conta            │
└──────────────────────────────────────────────┘
```

### [T-04b] Recuperar senha [F0]
```
┌──────────────────────────────────────────────┐
│ Recuperar senha                              │
├──────────────────────────────────────────────┤
│ Informe seu email. Enviaremos um link.       │
│                                              │
│ Email           [_______________________]    │
│                                              │
│        [ Enviar link ]                       │
│                                              │
│ ← Voltar pro login                           │
└──────────────────────────────────────────────┘
```

### [T-40] Configuracoes da conta [F1]
```
┌─────────────────────────────────────────────────┐
│ Configuracoes                                    │
├─────────────────────────────────────────────────┤
│ Perfil                                           │
│   Nome      [Rafael Dias]                        │
│   Email     rafa@x   [Alterar]                   │
│   Senha     ********  [Alterar]                  │
│                                                  │
│ Preferencias                                     │
│   Idioma    [PT-BR ▼]                            │
│   Tema      [Sistema ▼]                          │
│   Unidades  [SI (kN, m, MPa) ▼]                  │
│                                                  │
│ Plano                                            │
│   Atual: Pro · R$ XXX/mes        [Gerenciar]     │
│                                                  │
│ Sessao                                           │
│   [Sair de todos os dispositivos]                │
│   [Excluir conta]                                │
└─────────────────────────────────────────────────┘
```

### [T-70] Billing / Upgrade [F2]
```
┌─────────────────────────────────────────────────────────────┐
│ Planos                                                       │
├─────────────────────────────────────────────────────────────┤
│  Free          Pro            Studio          Enterprise    │
│  R$ 0          R$ XXX/mes     R$ XXX/mes      sob demanda   │
│  ─────         ──────         ──────          ──────        │
│  3 proj/mes    ilimitado      ilimitado       ilimitado     │
│  marca dagua   sem marca      multi-user      on-premise    │
│  sem BIM       BIM exp        workspace       SLA           │
│                API leitura    API completa    integracoes   │
│                               webhook         treinamento   │
│  [Atual]       [Upgrade]      [Upgrade]       [Falar conosco]│
└─────────────────────────────────────────────────────────────┘
```

### [T-80] Erro generico (4xx/5xx) [F0]
```
┌──────────────────────────────────────────────┐
│  ⚠ Algo deu errado                            │
│                                              │
│  [Mensagem amigavel do erro]                 │
│  Codigo: ERR-2026-0531-A1B2                  │
│                                              │
│  Tente:                                      │
│   · Recarregar a pagina                      │
│   · Voltar e tentar novamente                │
│   · Reportar pra suporte                     │
│                                              │
│  [Recarregar]  [Voltar]  [Reportar]          │
└──────────────────────────────────────────────┘
```

### [T-90] Confirmacao de email [F0]
```
┌──────────────────────────────────────────────┐
│  📧 Confirme seu email                        │
│                                              │
│  Enviamos um link pra rafa@x.                │
│  Clique pra ativar a conta.                  │
│                                              │
│  Nao recebeu?                                │
│  [Reenviar email]                            │
│                                              │
│  Mudou de email? [Trocar]                    │
└──────────────────────────────────────────────┘
```

### [T-30v] Detalhe de pilar [F1]
Igual T-30 detalhe viga mas com: esbeltez λ, λlim, indices de momentos minimos NBR 6118 §15.8, flexo-compressao oblqua (Mxd, Myd), armadura longitudinal + estribos, classificacao do pilar (curto/medio/esbelto).

### [T-30l] Detalhe de laje [F2]
Esforcos por faixa, armadura positiva/negativa, flecha (modulo Ec equivalente, fissuracao estadio II), wk, vibracao se necessario.

### [T-30c] Comparacao de versoes do projeto [F1]
Side-by-side de 2 versoes do mesmo projeto. Diff de elementos modificados, esforcos, dimensionamento, materiais. Util para "antes vs depois do override".

### Comportamento mobile do wizard
Em viewport < 768px:
- Cada um dos 5 passos vira full-screen.
- Stepper no topo encolhe (so o numero atual + total).
- Botoes "voltar / proximo" fixados no rodape.
- Inputs de geometria viram colunas empilhadas.
- Preview 2D da planta vira opcional (botao "ver planta") em modal.

---

## Critérios de aceitação UX (vão pra checklist do tester)

- [ ] Wizard leigo concluído em < 10 min com inputs reais (cronometrar 3 usuários)
- [ ] Toda inferência (vento, sismo, carga acidental, default normativo) é visível e ajustável
- [ ] Toda verificação cita norma + item explicitamente
- [ ] Erro de norma sempre vem com sugestão acionável
- [ ] PDF abre em < 3s e tem citação inline em cada cálculo
- [ ] Modo PRO não mostra wizard nunca, mas leigo pode "promover" projeto pra PRO
- [ ] Mobile: dashboard + relatório legíveis em 360px
