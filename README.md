# Assistente-Pessoal-Local-em-Python

# 🤖 J.A.R.V.I.S 2.0 — Assistente Pessoal Local em Python

J.A.R.V.I.S é um assistente pessoal desenvolvido em **Python**, integrado ao **Ollama + Llama 3.2**, capaz de interpretar comandos em linguagem natural, executar automações no Windows, realizar pesquisas e armazenar informações localmente.

O projeto foi desenvolvido como parte dos meus estudos em **Python, Inteligência Artificial e Automação**, com foco na aplicação prática dos conhecimentos adquiridos.

## 🧠 Como funciona

O projeto utiliza três componentes principais:

* **Python** — responsável pela lógica, automações e execução das ações.
* **Ollama + Llama 3.2** — responsável pela interpretação de linguagem natural e conversação.
* **JSON** — utilizado como sistema simples de memória persistente.

O modelo de IA não executa comandos diretamente.

Primeiro, o JARVIS interpreta o que o usuário deseja fazer e classifica a intenção. Depois, o Python decide qual função deve ser executada.

Exemplo:

```text
Usuário:
Abra o bloco de notas

IA:
{
    "acao": "abrir_programa",
    "alvo": "bloco de notas"
}

Python:
Executa o bloco de notas.
```

## ⚙️ Funcionalidades

Atualmente o JARVIS consegue:

*  Conversar utilizando IA local
*  Armazenar informações sobre o usuário
*  Abrir sites
*  Abrir programas do Windows
*  Realizar pesquisas no Google
*  Informar horário
*  Informar data
*  Abrir o explorador de arquivos
*  Abrir PowerShell e CMD
*  Abrir VS Code
*  Abrir calculadora
*  Abrir Paint
*  Informar status dos módulos
*  Interpretar comandos em linguagem natural

##  Exemplos de comandos

```text
Abra o Google

Abra o YouTube

Abra o GitHub

Abra o bloco de notas

Quero fazer algumas contas

Abra o VS Code

Pesquise cursos gratuitos de Python

Que horas são?

Qual é a data de hoje?

Lembre que meu nome é Shiro

O que você lembra sobre mim?

Status

Sair
```

##  Tecnologias utilizadas

* Python 3
* Ollama
* Llama 3.2
* Requests
* JSON
* Regex
* Subprocess
* Webbrowser

##  Estrutura

```text
JARVIS-Python/
│
├── main.py
├── README.md
├── requirements.txt
├── memoria.example.json
├── .gitignore
├── LICENSE
│
└── docs/
```

##  Como executar

### 1. Clone o projeto

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta:

```bash
cd JARVIS-Python
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Instale o Ollama

O projeto utiliza o Ollama para executar a inteligência artificial localmente.

Depois de instalar o Ollama, baixe o modelo:

```bash
ollama pull llama3.2
```

Execute:

```bash
ollama run llama3.2
```

### 5. Execute o JARVIS

```bash
python main.py
```

## 🔒 Privacidade

O projeto utiliza IA executada localmente através do Ollama.

As informações memorizadas pelo JARVIS são armazenadas localmente em um arquivo JSON.

O arquivo pessoal `memoria.json` não é enviado para o GitHub.

## 🗺️ Roadmap

Algumas funcionalidades que pretendo implementar futuramente:

*  Reconhecimento de voz
*  Respostas por voz
*  Interface gráfica
*  Consulta de clima
*  Gerenciamento de arquivos
*  Controle de músicas
*  Arquitetura modular
*  Histórico de conversas
*  Novas automações
*  Sistema de memória aprimorado

##  Objetivo do projeto

Este projeto faz parte do meu processo de aprendizado e transição profissional para a área de Tecnologia.

Meu objetivo é aplicar na prática conceitos de:

* Python
* Lógica de programação
* APIs
* Inteligência Artificial
* Automação
* Manipulação de JSON
* Processamento de linguagem natural
* Desenvolvimento de software

O projeto continuará sendo atualizado conforme avanço nos meus estudos.

---

### 👨‍💻 Desenvolvedor

Desenvolvido por **Bruno Dantas**

Estudante de Análise e Desenvolvimento de Sistemas, interessado em Python, Inteligência Artificial, automação e desenvolvimento de software.
