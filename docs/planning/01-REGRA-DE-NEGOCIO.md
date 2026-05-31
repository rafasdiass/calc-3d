---
documento: regra de negócio
versao: 1.0
data: 2026-05-31
status: ativa
substitui: README.md (que descrevia "LCT Calculator" desktop)
---

# 01 — REGRA DE NEGÓCIO

## Visão (1 frase)

Backend de cálculo estrutural multi-material que entrega **resultado normativo confiável com o mínimo de input possível**, e oferece **override paramétrico completo** quando o profissional precisa.

## Missão

Eliminar a barreira entre "engenheiro júnior / construtor / projetista" e "software de cálculo profissional". Hoje a escolha é binária: ou planilha imprecisa, ou TQS/SAP2000 com curva de aprendizado de meses e licença que custa R$ 15-50k/ano.

## Problema (que estamos resolvendo)

1. **Software estrutural profissional é caro** — TQS, Eberick, CYPE, SAP2000 cobram licença anual cara, modular (cada módulo extra = custo extra).
2. **Curva de aprendizado é alta** — pra calcular uma residência simples o usuário precisa entender FEM, modelagem, lançamento, várias normas.
3. **Geotecnia é desacoplada** — quem calcula fundação usa Geo5/Plaxis, quem calcula estrutura usa SAP/RFEM. Integração solo↔estrutura é manual e propensa a erro.
4. **Não tem SaaS web nativo** — todos os concorrentes principais são desktop Windows. Trabalho remoto, mobile, colaboração em tempo real ficam impossíveis.
5. **Input excessivo** — softwares atuais pedem dezenas de parâmetros que o engenheiro não tem em mãos no início do projeto. Falta camada de "pré-dimensionamento" inteligente.

## Solução (que estamos entregando)

### Princípio único

> **Quanto menos o usuário precisa digitar, mais o sistema precisa saber.**

A precisão **não** vem de pedir mais input. Vem de:
1. **defaults normativos inteligentes** (NBR 6118 manda γc=1.4? assume. usuário pode override.)
2. **inferência por contexto** (CEP → mapa de vento, velocidade básica → carga de vento. CEP → zona sísmica. tipo de obra → carga acidental NBR 6120.)
3. **bibliotecas embutidas** (perfis de aço comerciais BR/global, classes de concreto, tipos de solo de manuais geotécnicos brasileiros)
4. **validação cruzada** (avisar quando combinação de inputs viola norma — ex: pilar com ρ < ρmín NBR 6118)

### Duas camadas de uso

#### Camada Simples (LEIGO/JÚNIOR)
- Wizard guiado: tipo de obra → geometria básica → carga estimada
- Inferência automática de tudo que não foi informado
- Resultado: dimensionamento normativo + relatório técnico assinável
- Caso de uso: residência uni/multifamiliar até 4 pavimentos, galpão simples, muro de arrimo

#### Camada Profissional (PRO)
- Acesso paramétrico total: cada coeficiente, cada combinação de carga, cada método
- Override de qualquer default normativo (com justificativa registrada)
- Importação BIM (IFC 4.3), exportação pra TQS/CYPE/Robot via formatos abertos
- API pública pra automação (Grasshopper, scripts)
- Caso de uso: edifícios médios/altos, obras industriais, projetos especiais

## Escopo de cálculo (o que entregamos)

### Estrutural
- **Concreto armado** (NBR 6118, Eurocode 2, ACI 318): vigas, pilares, lajes (maciça e nervurada), fundações, pilar-parede
- **Aço** (NBR 8800, Eurocode 3, AISC 360): perfis laminados/soldados, ligações simples, treliças
- **Madeira** (NBR 7190, Eurocode 5): pórticos, treliças residenciais
- **Alvenaria estrutural** (NBR 16868) — v2

### Geotécnica (diferencial)
- **Capacidade de carga**: Terzaghi, Meyerhof, Vesic, Brinch-Hansen
- **Recalque**: elástico, Schmertmann, consolidação Terzaghi
- **Correlações SPT**: Décourt-Quaresma, Aoki-Velloso, Teixeira
- **Correlações CPT**: Schmertmann, Bustamante & Gianeselli
- **Perfil estratigráfico**: até N camadas, propriedades por camada
- **Tipos de solo**: argila (mole/média/rija/dura), areia (fofa/medianamente compacta/compacta), silte, rocha — biblioteca com defaults brasileiros

### Análises
- **Estática linear** (MVP)
- **Estática com não-linearidade física** (concreto fissurado) — v1.5
- **Dinâmica modal + sísmica** (NBR 15421, Eurocode 8) — v2
- **Vento** (NBR 6123) com inferência de vb por CEP — MVP
- **Térmica** — v3

### Saídas
- **Relatório técnico PDF** assinável (memória de cálculo passo-a-passo, citações de norma, gráficos 2D)
- **Planta de fôrma e armação** em DXF/PDF — v1.5
- **Lista de materiais** (quantitativos)
- **JSON estruturado** pra integração com BIM/ERP

## Escopo do NÃO-fazer (explícito)

- **Não** vamos renderizar 3D in-app. Esquemas 2D, sim. Modelo 3D interativo, não. Quem quer ver em 3D, exporta IFC e abre no BIM viewer dele.
- **Não** vamos fazer detalhamento gráfico avançado (lançamento por arrastar elementos no canvas). Input é tabular/wizard.
- **Não** vamos resolver casca, membrana, problemas de mecânica do contínuo avançada. FEM é frame + shell simples.
- **Não** vamos competir em performance bruta com SAP2000 pra modelos > 10k nós. Nicho é projeto cotidiano, não obra de arte especial.

## Modelo de negócio

### Tier Free
- 3 projetos/mês
- Relatório com marca d'água
- Sem exportação BIM

### Tier Pro (engenheiro autônomo)
- Projetos ilimitados
- Sem marca d'água
- Exportação BIM, DXF, JSON
- Suporte por email

### Tier Studio (escritório)
- Múltiplos usuários
- Workspace compartilhado
- API pública
- Suporte prioritário

### Tier Enterprise (construtora/governo)
- On-premise opcional
- SLA
- Integrações custom
- Treinamento

(Preços a definir após validação do research.)

## KPIs de produto

| KPI | Meta v1 (12 meses) |
|---|---|
| Tempo médio pra primeiro cálculo válido (novo usuário leigo) | < 10 minutos |
| Tempo médio pra primeiro cálculo válido (PRO migrando do TQS) | < 1 hora |
| % de cálculos sem necessidade de override de default normativo | > 70% |
| Cobertura de NBR 6118 (capítulos críticos) | 100% |
| Cobertura de NBR 6122 (todos os tipos de fundação relevantes) | 100% |
| Conversão free → pro | > 8% |

## Compliance e responsabilidade técnica

- Software gera **memória de cálculo**, não ART. ART é do engenheiro responsável.
- Citação inequívoca de norma e fórmula em cada cálculo.
- Versionamento de norma (NBR 6118:2014 vs futuras revisões) — usuário escolhe qual aplicar.
- Log auditável: quem calculou, quando, com quais parâmetros, qual versão do motor.

## Diferenciais defensáveis

1. **Camada simples real** — não é "modo iniciante" disfarçado, é cálculo completo com defaults normativos transparentes.
2. **Geotecnia + estrutura no mesmo motor** — interação solo-estrutura nativa, sem export-import entre softwares.
3. **SaaS web first** — colaboração, mobile, sem instalação, sem licença Windows.
4. **NBR + Eurocode + ACI nativos** — engenheiro que faz projeto BR e exporta consultoria pra fora não precisa trocar de software.
5. **Preço acessível** — escala SaaS permite ordem de grandeza menor que TQS/Eberick.
6. **API aberta** — diferencial vs TQS (caixa fechada). Permite ecossistema de plugins, integração com Grasshopper, scripts customizados de escritório.
7. **Caveat de marketing — madeira**: o argumento "Eberick nao tem madeira" baseia-se em ausencia na pagina oficial de produto (snapshot 2026-05-31). Confirmar em escritorio que use Eberick antes de uso comercial. Detalhe em `10-RESEARCH-COMPETITIVO.md` secao H.
