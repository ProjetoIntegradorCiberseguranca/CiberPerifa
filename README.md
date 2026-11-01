# CiberPerifa

**Educação em cibersegurança e conscientização digital para todos.**

O CiberPerifa é um projeto desenvolvido como parte da disciplina Projeto Integrador no primeiro semestre do curso de Análise e Desenvolvimento de Sistemas da Fatec São Paulo. Seu objetivo é promover a conscientização sobre segurança digital, oferecendo informações educativas e acessíveis sobre ameaças cibernéticas e formas de proteção na internet.

O projeto também disponibiliza uma cartilha em PDF, gerada dinamicamente com informações sobre vulnerabilidades conhecidas e recomendações de segurança.

## Sobre o projeto

O CiberPerifa busca tornar o conhecimento sobre cibersegurança mais acessível, ajudando os usuários a reconhecer ameaças digitais, proteger seus dados pessoais e desenvolver hábitos mais seguros no ambiente online.

A iniciativa foi desenvolvida em colaboração com a organização parceira "Perifa na Lista", considerando a importância da inclusão digital e do acesso à informação.

## Funcionalidades

- **Conteúdo educativo:** informações sobre segurança digital, ameaças cibernéticas e proteção de dados.
- **Cartilha em PDF:** geração dinâmica de um documento educativo para consulta e download.
- **Informações sobre vulnerabilidades:** consulta ao catálogo Known Exploited Vulnerabilities (KEV), mantido pela CISA.
- **Explicações simplificadas:** apresentação de explicações educativas para facilitar a compreensão de vulnerabilidades técnicas.
- **Interface responsiva:** adaptação do site a diferentes tamanhos de tela.
- **Modo claro e escuro:** opção para alternar entre os temas visuais.

## Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Lógica e funcionalidades do sistema |
| Flask | Desenvolvimento do servidor e das rotas |
| HTML5 | Estrutura das páginas |
| CSS3 | Estilização e responsividade |
| JavaScript | Interatividade da interface |
| ReportLab | Geração dos documentos PDF |
| Requests | Comunicação com APIs externas |
| Vercel | Hospedagem e publicação do projeto |

## Fonte de dados

O projeto utiliza o catálogo **Known Exploited Vulnerabilities (KEV)**, disponibilizado pela CISA (Cybersecurity and Infrastructure Security Agency), agência do governo dos Estados Unidos responsável pela segurança cibernética e proteção de infraestruturas críticas.

O catálogo reúne vulnerabilidades que possuem evidências de exploração em situações reais.

**Fonte oficial:** [CISA - Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**API utilizada:** [CISA KEV JSON Feed](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json)

## Como executar localmente

### Pré-requisitos

- Python instalado.
- Git instalado.
- Visual Studio Code ou outro editor de código.

### 1. Clone o repositório

```bash
git clone https://github.com/ProjetoIntegradorCiberseguranca/CiberPerifa.git
```

### 2. Acesse a pasta do projeto

```bash
cd CiberPerifa
```

### 3. Crie um ambiente virtual

```bash
python -m venv .venv
```

### 4. Ative o ambiente virtual

No Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

No Linux:

```bash
source .venv/bin/activate
```

### 5. Instale as dependências

```bash
pip install -r requirements.txt
```

### 6. Execute a aplicação

```bash
python app.py
```

Após iniciar o servidor, acesse:

http://127.0.0.1:5000

**Observação:** a geração da cartilha depende de conexão com a internet para consultar os dados disponibilizados pela CISA.

## Estrutura do projeto

```text
CiberPerifa/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── templates/
│   ├── index.html
│   └── sobre.html
│
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── script.js
    └── img/
        └── logo-perifa.png
```

## Acesse o projeto

**Site publicado:** https://ciber-perifa.vercel.app/

**Repositório:** https://github.com/ProjetoIntegradorCiberseguranca/CiberPerifa

---

Desenvolvido como Projeto Integrador no primeiro semestre do curso de Análise e Desenvolvimento de Sistemas da Fatec São Paulo.