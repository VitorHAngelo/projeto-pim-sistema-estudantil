import json
import os
from paths import FILES_PATH
from seguranca import get_fernet

USERS_FILE = "usuarios.json"


def checar_json_existe():
    if not os.path.exists(FILES_PATH + USERS_FILE):  # Se não existir
        print("Criando database.")

        with open(FILES_PATH + USERS_FILE, mode="wb") as file:  # Cria arquivo
            dados_protegidos = get_fernet().encrypt("{}".encode())
            file.write(dados_protegidos)

    else:
        print("Arquivo JSON já presente.")


def descriptografar_json(arquivo="usuarios.json"):
    with open(FILES_PATH + arquivo, mode="rb") as file:
        dados_protegidos = file.read()

        return json.loads(get_fernet().decrypt(dados_protegidos).decode())


def criptografar_json(dados, arquivo="usuarios.json"):
    with open(FILES_PATH + USERS_FILE, mode="wb") as file:  # Cria arquivo
        dados_bytes = json.dumps(dados).encode()
        dados_protegidos = get_fernet().encrypt(dados_bytes)
        file.write(dados_protegidos)


def get_colaborador(identificador):
    """Espera receber o identificador do usuário e retorna suas informações

    Args:
        identificador (str): Identificador geral do usuário

    Returns:
        dict: Informações do usuário
    """
    dados = descriptografar_json()
    if not identificador in dados:
        print("Usuário não localizado no sistema.")
        return None
    else:
        return {"cpf": identificador, **dados[identificador]}


def get_aluno():
    pass


def add_colaborador(usuario: dict) -> str:
    """Recebe um dicionário e verifica a por ocorrência no banco atual, formata devidamente e salva no JSON.

    Args:
        usuario (dict): Informações do usuário

    Returns:
        str: Informativo do status da operação
    """
    if not usuario:
        return (0, "Usuário inválido.")
    for identificador, informacoes in usuario.items():
        break
    colaborador = get_colaborador(identificador)
    if colaborador != None:
        return (1, f"Usuário {colaborador[identificador]['nome']} já está cadastrado.")
    else:
        dados = descriptografar_json()
        dados[identificador] = informacoes
        criptografar_json(dados=dados)
        return (2, "Usuário cadastrado.")


def editar_colaborador(usuario: dict) -> str:
    """Recebe um dicionário com os dados do usuário e atualiza o arquivo JSON.

    Args:
        usuario (dict): Informações do usuário

    Returns:
        str: Informativo do status da operação
    """
    dados = descriptografar_json()
    for identificador, informacoes in usuario.items():
        break
    dados[identificador] = informacoes
    criptografar_json(dados=dados)
    return f"Perfil atualizado."


def cadastrar():
    pass
