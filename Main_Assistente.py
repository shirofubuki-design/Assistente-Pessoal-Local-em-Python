import datetime
import json
import os
import random
import re
import subprocess
import webbrowser

import requests


# =========================================================
# J.A.R.V.I.S - ASSISTENTE PESSOAL LOCAL
# Versão 2.0
#
# Python = corpo / automação
# Ollama + Llama 3.2 = cérebro
# JSON = memória
# =========================================================


NOME = "JARVIS"

OLLAMA_URL = "http://localhost:11434/api/chat"
MODELO = "llama3.2"

ARQUIVO_MEMORIA = "memoria.json"


# =========================================================
# CONFIGURAÇÕES
# =========================================================

SITES = {#Esse sinal de hash indica que o dicionário SITES contém os sites que o Jarvis pode abrir. A chave é o nome do site e o valor é a URL correspondente.
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "linkedin": "https://www.linkedin.com",
    "stackoverflow": "https://stackoverflow.com",
}


PROGRAMAS = {
    "bloco de notas": "notepad.exe",
    "notepad": "notepad.exe",

    "paint": "mspaint.exe",

    "gerenciador de tarefas": "taskmgr.exe",

    "explorador de arquivos": "explorer.exe",
    "explorador": "explorer.exe",

    "powershell": "powershell.exe",

    "cmd": "cmd.exe",
    "prompt de comando": "cmd.exe",

    # Para VS Code funcionar com "code",
    # o comando precisa estar configurado no PATH.
    "vscode": "code",
    "visual studio code": "code",
}


# =========================================================
# MEMÓRIA
# =========================================================

def carregar_memoria():

    if os.path.exists(ARQUIVO_MEMORIA):#path é o caminho do arquivo, se existir, ele vai abrir e carregar a memória do Jarvis a partir do arquivo JSON. Se não existir, ele retorna um dicionário vazio.

        try:

            with open(
                ARQUIVO_MEMORIA,
                "r",
                encoding="utf-8"
            ) as arquivo:

                memoria_carregada = json.load(arquivo)

                if isinstance(memoria_carregada, dict):
                    return memoria_carregada

        except Exception as erro:

            print(
                f"\nErro ao carregar memória: {erro}"
            )

    return {
        "nome": "",
        "informacoes": []
    }


def salvar_memoria():

    try:

        with open(
            ARQUIVO_MEMORIA,
            "w",#w seria para escrita, se o arquivo não existir, ele cria um novo arquivo. Se existir, ele sobrescreve o conteúdo existente.
            encoding="utf-8" #utf-8 é para garantir que caracteres especiais sejam salvos corretamente no arquivo JSON.
        ) as arquivo:

            json.dump(
                memoria,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    except Exception as erro:

        print(
            f"\nErro ao salvar memória: {erro}"
        )


memoria = carregar_memoria()


# Garante compatibilidade caso exista
# uma memoria.json de versões antigas.

if "nome" not in memoria:
    memoria["nome"] = ""

if "informacoes" not in memoria:
    memoria["informacoes"] = []


# =========================================================
# RESPOSTAS
# =========================================================

def falar(mensagem):

    print(
        f"\n{NOME}: {mensagem}"
    )


def saudacao():

    hora = datetime.datetime.now().hour

    if hora < 12:
        return "Bom dia"

    elif hora < 18:
        return "Boa tarde"

    else:
        return "Boa noite"


# =========================================================
# FERRAMENTAS - SITES
# =========================================================

def abrir_site(nome):

    nome = nome.lower().strip()

    if nome in SITES:

        falar(
            f"Abrindo {nome}."
        )

        webbrowser.open(
            SITES[nome]
        )

        return True

    falar(
        f"Não encontrei o site '{nome}' "
        "na minha lista de sites permitidos."
    )

    return False


# =========================================================
# FERRAMENTAS - PROGRAMAS
# =========================================================

def abrir_programa(nome):

    nome = nome.lower().strip()

    # -----------------------------------------
    # CALCULADORA
    # -----------------------------------------

    if nome in [
        "calculadora",
        "calc"
    ]:

        falar(
            "Abrindo a calculadora."
        )

        os.system(
            "start calc"
        )

        return True

    # -----------------------------------------
    # OUTROS PROGRAMAS
    # -----------------------------------------

    if nome in PROGRAMAS:

        programa = PROGRAMAS[nome]

        falar(
            f"Abrindo {nome}."
        )

        try:

            subprocess.Popen(
                programa,
                shell=True
            )

            return True

        except Exception as erro:

            falar(
                f"Não consegui abrir {nome}."
            )

            print(
                f"Erro: {erro}"
            )

            return False

    falar(
        f"O programa '{nome}' ainda "
        "não está configurado."
    )

    return False


# =========================================================
# PESQUISA GOOGLE
# =========================================================

def pesquisar_google(pesquisa):

    pesquisa = pesquisa.strip()

    if not pesquisa:

        falar(
            "Preciso saber o que você deseja pesquisar."
        )

        return

    falar(
        f"Pesquisando por {pesquisa}."
    )

    pesquisa_url = pesquisa.replace(
        " ",
        "+"
    )

    url = (
        "https://www.google.com/search?q="
        + pesquisa_url
    )

    webbrowser.open(url)


# =========================================================
# DATA E HORA
# =========================================================

def informar_hora():

    hora = datetime.datetime.now().strftime(
        "%H:%M"
    )

    falar(
        f"Agora são {hora}."
    )


def informar_data():

    data = datetime.datetime.now().strftime(
        "%d/%m/%Y"
    )

    falar(
        f"Hoje é {data}."
    )


# =========================================================
# MEMÓRIA - APRENDER
# =========================================================

def memorizar(informacao):

    informacao = informacao.strip()

    if not informacao:

        falar(
            "Não encontrei nenhuma informação para memorizar."
        )

        return

    # -----------------------------------------
    # TENTAR IDENTIFICAR O NOME
    # -----------------------------------------

    resultado_nome = re.search(
        r"meu nome (?:é|e) ([a-zA-ZÀ-ÿ0-9_-]+)",
        informacao,
        re.IGNORECASE
    )

    if resultado_nome:

        nome_usuario = resultado_nome.group(1)

        memoria["nome"] = nome_usuario

        salvar_memoria()

        falar(
            f"Entendido. Vou lembrar que seu nome é "
            f"{nome_usuario}."
        )

        return

    # -----------------------------------------
    # OUTRAS INFORMAÇÕES
    # -----------------------------------------

    if informacao not in memoria["informacoes"]:

        memoria["informacoes"].append(
            informacao
        )

        salvar_memoria()

        falar(
            "Informação armazenada na memória."
        )

    else:

        falar(
            "Essa informação já está armazenada."
        )


# =========================================================
# CONSULTAR MEMÓRIA
# =========================================================

def mostrar_memoria():

    nome_usuario = memoria.get(
        "nome",
        ""
    )

    informacoes = memoria.get(
        "informacoes",
        []
    )

    if not nome_usuario and not informacoes:

        falar(
            "Minha memória ainda está vazia."
        )

        return

    falar(
        "Estas são as informações que tenho armazenadas:"
    )

    if nome_usuario:

        print(
            f"  • Nome: {nome_usuario}"
        )

    for informacao in informacoes:

        print(
            f"  • {informacao}"
        )


# =========================================================
# CONTEXTO DE MEMÓRIA PARA A IA
# =========================================================

def gerar_contexto_memoria():

    contexto = []

    if memoria.get("nome"):

        contexto.append(
            f"O nome do usuário é {memoria['nome']}."
        )

    for informacao in memoria.get(
        "informacoes",
        []
    ):

        contexto.append(
            informacao
        )

    if not contexto:

        return "Nenhuma informação pessoal armazenada."

    return "\n".join(contexto)


# =========================================================
# IA - INTERPRETAR INTENÇÃO
# =========================================================

def interpretar_comando_ia(comando):

    memoria_usuario = gerar_contexto_memoria()

    prompt_sistema = f"""
Você é o módulo de interpretação de comandos do JARVIS.

Você recebe uma frase em português do Brasil e deve decidir
qual ação o usuário deseja executar.

Você NÃO executa comandos.

Você apenas classifica a intenção.

Informações conhecidas sobre o usuário:

{memoria_usuario}


Ações permitidas:

abrir_site
abrir_programa
pesquisar_google
hora
data
memorizar
mostrar_memoria
status
conversar
sair


Sites disponíveis:

google
youtube
github
linkedin
stackoverflow


Programas disponíveis:

bloco de notas
calculadora
paint
gerenciador de tarefas
explorador de arquivos
powershell
cmd
vscode


Responda SOMENTE em JSON. #resposta deve ser em json por que o Jarvis vai interpretar a resposta e executar a ação correspondente. Se você não souber qual ação executar, use "conversar".

Formato:

{{
    "acao": "nome_da_acao",
    "alvo": "alvo_da_acao",
    "mensagem": ""
}}


Exemplos:


Usuário:
"abre o google"

Resposta:

{{
    "acao": "abrir_site",
    "alvo": "google",
    "mensagem": ""
}}


Usuário:
"abre o bloco de notas para mim"

Resposta:

{{
    "acao": "abrir_programa",
    "alvo": "bloco de notas",
    "mensagem": ""
}}


Usuário:
"quero fazer algumas contas"

Resposta:

{{
    "acao": "abrir_programa",
    "alvo": "calculadora",
    "mensagem": ""
}}


Usuário:
"pesquise cursos de python"

Resposta:

{{
    "acao": "pesquisar_google",
    "alvo": "cursos de python",
    "mensagem": ""
}}


Usuário:
"que horas são?"

Resposta:

{{
    "acao": "hora",
    "alvo": "",
    "mensagem": ""
}}


Usuário:
"que dia é hoje?"

Resposta:

{{
    "acao": "data",
    "alvo": "",
    "mensagem": ""
}}


Usuário:
"lembre que meu nome é Shiro"

Resposta:

{{
    "acao": "memorizar",
    "alvo": "meu nome é Shiro",
    "mensagem": ""
}}


Usuário:
"o que você lembra sobre mim?"

Resposta:

{{
    "acao": "mostrar_memoria",
    "alvo": "",
    "mensagem": ""
}}


Se o usuário apenas quiser conversar,
perguntar algo de programação,
tecnologia ou outro assunto,
use:

{{
    "acao": "conversar",
    "alvo": "",
    "mensagem": ""
}}
"""

    dados = {

        "model": MODELO,

        "messages": [

            {
                "role": "system",
                "content": prompt_sistema
            },

            {
                "role": "user",
                "content": comando
            }
        ],

        "stream": False,

        "format": "json"
    }

    try:

        resposta = requests.post(
            OLLAMA_URL,
            json=dados,
            timeout=60
        )

        resposta.raise_for_status()

        resultado = resposta.json()

        conteudo = resultado[
            "message"
        ][
            "content"
        ]

        return json.loads(
            conteudo
        )

    except requests.exceptions.ConnectionError:

        falar(
            "Não consegui me conectar ao Ollama."
        )

        return None

    except Exception as erro:

        print(
            f"\nErro ao interpretar comando: {erro}"
        )

        return None


# =========================================================
# IA - CONVERSA NORMAL
# =========================================================

def conversar_com_ia(pergunta):

    memoria_usuario = gerar_contexto_memoria()

    prompt_sistema = f"""
Você é JARVIS, um assistente pessoal local.

Seu nome é JARVIS.

Você fala português do Brasil.

Sua personalidade é:

- inteligente
- educada
- objetiva
- tecnológica
- prestativa
- humor sutil

Você ajuda principalmente com:

- programação
- Python
- tecnologia
- estudos
- computadores

Você está rodando localmente através do Ollama.

Nunca diga que executou alguma ação no computador
se você não executou.

Informações conhecidas sobre o usuário:

{memoria_usuario}
"""

    dados = {

        "model": MODELO,

        "messages": [

            {
                "role": "system",
                "content": prompt_sistema
            },

            {
                "role": "user",
                "content": pergunta
            }
        ],

        "stream": False
    }

    try:

        resposta = requests.post(
            OLLAMA_URL,
            json=dados,
            timeout=120
        )

        resposta.raise_for_status()

        resultado = resposta.json()

        resposta_jarvis = resultado[
            "message"
        ][
            "content"
        ]

        falar(
            resposta_jarvis
        )

    except requests.exceptions.ConnectionError:

        falar(
            "Meu núcleo de inteligência está offline. "
            "Verifique se o Ollama está funcionando."
        )

    except Exception as erro:

        falar(
            "Ocorreu um erro ao consultar meu núcleo "
            "de inteligência."
        )

        print(
            f"Erro: {erro}"
        )


# =========================================================
# EXECUTAR AÇÃO INTERPRETADA PELA IA
# =========================================================

def executar_acao(resultado, comando_original):

    if not resultado:

        falar(
            "Não consegui interpretar esse comando."
        )

        return True

    acao = resultado.get(
        "acao",
        "conversar"
    )

    alvo = resultado.get(
        "alvo",
        ""
    )

    # -----------------------------------------
    # ABRIR SITE
    # -----------------------------------------

    if acao == "abrir_site":

        abrir_site(
            alvo
        )

    # -----------------------------------------
    # ABRIR PROGRAMA
    # -----------------------------------------

    elif acao == "abrir_programa":

        abrir_programa(
            alvo
        )

    # -----------------------------------------
    # PESQUISAR
    # -----------------------------------------

    elif acao == "pesquisar_google":

        pesquisar_google(
            alvo
        )

    # -----------------------------------------
    # HORA
    # -----------------------------------------

    elif acao == "hora":

        informar_hora()

    # -----------------------------------------
    # DATA
    # -----------------------------------------

    elif acao == "data":

        informar_data()

    # -----------------------------------------
    # MEMORIZAR
    # -----------------------------------------

    elif acao == "memorizar":

        memorizar(
            alvo
        )

    # -----------------------------------------
    # MOSTRAR MEMÓRIA
    # -----------------------------------------

    elif acao == "mostrar_memoria":

        mostrar_memoria()

    # -----------------------------------------
    # STATUS
    # -----------------------------------------

    elif acao == "status":

        falar(
            "Todos os sistemas estão operacionais. "
            "Núcleo Llama 3.2 online. "
            "Memória online. "
            "Módulo de automação online."
        )

    # -----------------------------------------
    # CONVERSAR
    # -----------------------------------------

    elif acao == "conversar":

        conversar_com_ia(
            comando_original
        )

    # -----------------------------------------
    # SAIR
    # -----------------------------------------

    elif acao == "sair":

        falar(
            "Encerrando sistemas. Até mais."
        )

        return False

    else:

        conversar_com_ia(
            comando_original
        )

    return True


# =========================================================
# COMANDOS DIRETOS
#
# Esses comandos não precisam consultar a IA.
# Assim a resposta fica mais rápida.
# =========================================================

def comando_direto(comando):

    comando_limpo = comando.lower().strip()

    # -----------------------------------------
    # SAUDAÇÃO
    # -----------------------------------------

    if comando_limpo in [
        "oi",
        "olá",
        "ola",
        "bom dia",
        "boa tarde",
        "boa noite"
    ]:

        respostas = [

            f"{saudacao()}. Como posso ajudá-lo?",

            f"{saudacao()}. Estou pronto.",

            f"{saudacao()}. Sistemas online."
        ]

        falar(
            random.choice(
                respostas
            )
        )

        return True

    # -----------------------------------------
    # AJUDA
    # -----------------------------------------

    if comando_limpo == "ajuda":

        falar(
            "Você pode conversar comigo naturalmente."
        )

        print(
            """
Exemplos:

  • Abra o Google
  • Abra o YouTube
  • Abra o GitHub
  • Abra o bloco de notas
  • Abra a calculadora
  • Quero fazer algumas contas
  • Abra o Paint
  • Abra o explorador de arquivos
  • Abra o VS Code
  • Pesquise cursos gratuitos de Python
  • Que horas são?
  • Qual é a data de hoje?
  • Lembre que meu nome é Shiro
  • O que você lembra sobre mim?
  • Status
  • Sair
"""
        )

        return True

    return False


# =========================================================
# INICIALIZAÇÃO
# =========================================================

def iniciar():

    print(
        "=" * 60
    )

    print(
        "                   J.A.R.V.I.S 2.0"
    )

    print(
        "=" * 60
    )

    print()

    print(
        "Sistema inicializado."
    )

    print(
        f"Núcleo de inteligência: {MODELO}"
    )

    print(
        "Processamento: LOCAL"
    )

    print(
        "Memória: ONLINE"
    )

    print(
        "Automação: ONLINE"
    )

    print()

    print(
        "Digite 'ajuda' para visualizar exemplos."
    )

    print(
        "Digite 'sair' para encerrar."
    )

    print(
        "=" * 60
    )

    while True:

        try:

            comando = input(
                "\nVocê: "
            )

        except KeyboardInterrupt:

            falar(
                "Encerrando sistemas."
            )

            break

        if not comando.strip():

            continue

        comando_normalizado = comando.lower().strip()

        # -----------------------------------------
        # SAIR IMEDIATAMENTE
        # -----------------------------------------

        if comando_normalizado in [
            "sair",
            "exit",
            "encerrar",
            "desligar"
        ]:

            falar(
                "Encerrando sistemas. Até mais."
            )

            break

        # -----------------------------------------
        # COMANDOS RÁPIDOS
        # -----------------------------------------

        if comando_direto(
            comando
        ):

            continue

        # -----------------------------------------
        # IA INTERPRETA
        # -----------------------------------------

        resultado = interpretar_comando_ia(
            comando
        )

        continuar = executar_acao(
            resultado,
            comando
        )

        if not continuar:
            break


# =========================================================
# EXECUTAR
# =========================================================

if __name__ == "__main__":

    iniciar()