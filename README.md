

```markdown
# LCT Calculator

LCT Calculator é um projeto desenvolvido para calcular diferentes tipos de fundações, gerar relatórios e sincronizar os dados com uma plataforma BIM. Ele utiliza o banco de dados SQLite para armazenar informações sobre cálculos, relatórios e status de sincronização.

## Funcionalidades

- **Cálculos de Fundações**: Calcule diferentes tipos de fundações, incluindo sapata, blocos, tubulões, etc.
- **Relatórios Automáticos**: Gere relatórios com base nos cálculos de fundações.
- **Sincronização com Plataforma BIM**: Sincronize os dados calculados com plataformas BIM para manter as informações atualizadas.
- **Armazenamento Persistente com SQLite**: Armazene dados de cálculos e relatórios localmente utilizando SQLite.

## Estrutura do Projeto

Abaixo está a estrutura do projeto com seus principais diretórios e arquivos:

```
lct_calculator/
│
├── src/
│   └── lct_calculator/
│       ├── __init__.py
│       ├── main.py
│       ├── database.py
│       ├── calculators/
│       │   ├── __init__.py
│       │   └── simple_interest_calculator.py
│       ├── helpers/
│       │   ├── __init__.py
│       │   └── calculation_helpers.py
│       ├── interfaces/
│       │   ├── __init__.py
│       │   └── tqs_integration.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── sqlite_service.py
│       │   └── bim_integration.py
│
├── tests/
│   ├── __init__.py
│   └── test_lct_calculator.py
│
├── venv/
│   └── ... (ambiente virtual)
│
├── README.md
├── setup.py
├── requirements.txt
└── .gitignore
```

## Instalação

Siga as instruções abaixo para configurar e rodar o projeto:

### 1. Clonando o Repositório

```bash
git clone https://github.com/seuusuario/lct_calculator.git
cd lct_calculator
```

### 2. Criando e Ativando o Ambiente Virtual

Crie e ative um ambiente virtual para isolar as dependências do projeto:

#### No MacOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### No Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalando Dependências

Com o ambiente virtual ativado, instale todas as dependências necessárias:

```bash
pip install -r requirements.txt
```

### 4. Inicializando o Banco de Dados

Antes de rodar o projeto, é necessário inicializar o banco de dados SQLite. Execute o script abaixo para criar as tabelas no banco de dados:

```bash
python src/lct_calculator/services/sqlite_service.py
```

Isso criará o arquivo `lct_calculator.db` com as seguintes tabelas:

- **fundacoes**: Armazena dados sobre as fundações calculadas.
- **relatorios**: Armazena relatórios gerados com base nas fundações calculadas.
- **sincronizacao_bim**: Armazena o status da sincronização dos dados com a plataforma BIM.

### 5. Rodando o Programa Principal

Após a instalação e configuração, você pode rodar o programa principal:

```bash
python src/lct_calculator/main.py
```

### 6. Gerando Relatórios

Você pode gerar relatórios automaticamente após realizar os cálculos de fundações. Esses relatórios serão armazenados na tabela `relatorios` do banco de dados.

### 7. Sincronizando com Plataforma BIM

Para sincronizar os dados calculados com uma plataforma BIM, execute o seguinte script:

```bash
python src/lct_calculator/services/bim_integration.py
```

Isso atualizará o status da sincronização na tabela `sincronizacao_bim`.

## Testes

Testes automatizados estão disponíveis no projeto. Para rodar os testes, use o comando:

```bash
python -m unittest discover -s tests
```

## Como Funciona

### Banco de Dados

O banco de dados SQLite é utilizado para armazenar as fundações calculadas, relatórios gerados e o status de sincronização com a plataforma BIM. Os dados persistentes permitem que os cálculos e os relatórios sejam acessados em execuções subsequentes.

### Integração com Plataforma BIM

A sincronização com uma plataforma BIM é simulada pelo arquivo `bim_integration.py`. Ele atualiza o status de sincronização dos dados de fundações, permitindo manter os dados do projeto sincronizados com o BIM.

### Cálculos de Fundações

Os cálculos de fundações são realizados utilizando o módulo `calculators`, onde diferentes tipos de fundações podem ser implementados.

## Dependências

O projeto utiliza as seguintes bibliotecas:

- **SQLite**: Para armazenamento local de dados.
- **Python 3.x**: Versão mínima recomendada 3.7.
- **Pyside2**: Para a criação da interface gráfica.

Todas as dependências necessárias estão listadas no arquivo `requirements.txt`.

## Criador

Este projeto foi criado e desenvolvido por **Rafael Dias**.

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE).

```

### Como Rodar o Programa com Interface
Para rodar o programa com a interface gráfica que você criou (usando `PySide2`), o arquivo principal (`main.py`) deve ter a lógica para iniciar a interface gráfica. No `README.md`, já foi incluída a explicação para rodar o programa com o comando:

```bash
python src/lct_calculator/main.py
```

