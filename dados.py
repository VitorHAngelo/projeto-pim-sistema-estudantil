import json
import os
from paths import FILES_PATH
from seguranca import get_fernet

FILE_NAMES = {
    "colaboradores": "colaboradores.json",
    "alunos": "alunos.json",
    "turmas": "turmas.json",
}


def checar_json_existe():
    for key, value in FILE_NAMES.items():
        if not os.path.exists(FILES_PATH + value):  # Se não existir
            print(f"Criando database {key}.")

            with open(FILES_PATH + value, mode="wb") as file:  # Cria arquivo
                dados_protegidos = get_fernet().encrypt("{}".encode())
                file.write(dados_protegidos)

        else:
            print(f"Arquivo {key} JSON já presente.")


def descriptografar_json(arquivo="colaboradores"):
    with open(FILES_PATH + FILE_NAMES[arquivo], mode="rb") as file:
        dados_protegidos = file.read()

        return json.loads(get_fernet().decrypt(dados_protegidos).decode())


def criptografar_json(dados, arquivo="colaboradores"):
    with open(FILES_PATH + str(FILE_NAMES[arquivo]), mode="wb") as file:  # Cria arquivo
        dados_bytes = json.dumps(dados).encode()
        dados_protegidos = get_fernet().encrypt(dados_bytes)
        file.write(dados_protegidos)


def get_colaborador(identificador):
    """Espera receber o identificador do docente e retorna suas informações

    Args:
        identificador (str): Identificador geral do docente

    Returns:
        dict: Informações do docente
    """
    dados = descriptografar_json("colaboradores")
    if not identificador in dados:
        print("Usuário não localizado no sistema.")
        return None
    else:
        return {"cpf": identificador, **dados[identificador]}


def get_aluno(identificador):
    """Espera receber o identificador do usuário e retorna suas informações

    Args:
        identificador (str): Identificador geral do usuário

    Returns:
        dict: Informações do usuário
    """
    dados = descriptografar_json("alunos")
    if not identificador in dados:
        print("Usuário não localizado no sistema.")
        return None
    else:
        return {"cpf": identificador, **dados[identificador]}


def add_colaborador(usuario: dict) -> str:
    """Recebe um dicionário e verifica a por ocorrência no banco atual, formata devidamente e salva no JSON.

    Args:
        usuario (dict): Informações do usuário

    Returns:
        str: Informativo do status da operação
    """
    if not usuario:
        return [0, "Usuário inválido."]
    for identificador, informacoes in usuario.items():
        break
    colaborador = get_colaborador(identificador)
    if colaborador != None:
        return [
            1,
            f"Usuário {colaborador[identificador]['nome']} já está cadastrado.",
        ]
    else:
        dados = descriptografar_json(arquivo="colaboradores")
        dados[identificador] = informacoes
        criptografar_json(dados=dados)
        return [2, "Usuário cadastrado."]


def editar_colaborador(colaborador: dict) -> str:
    """Recebe um dicionário com os dados do colaborador e atualiza o arquivo JSON.

    Args:
        colaborador (dict): Informações do colaborador

    Returns:
        str: Informativo do status da operação
    """
    dados = descriptografar_json(arquivo="colaboradores")
    dados[colaborador.pop("cpf")] = colaborador
    criptografar_json(dados=dados, arquivo="colaboradores")
    return f"Perfil atualizado."


def cadastrar():
    pass


def add_turma(turma: dict) -> str:
    """Recebe um dicionário e verifica a por ocorrência no banco atual, formata devidamente e salva no JSON.

    Args:
        turma (dict): Informações da turma

    Returns:
        str: Informativo do status da operação
    """
    if not turma:
        return [0, "Turma inválida."]
    for identificador, informacoes in turma.items():
        break
    turma = get_turma(identificador)
    if turma != None:
        return [
            1,
            f"{turma[identificador]['nome']} já está cadastrada.",
        ]
    else:
        dados = descriptografar_json(arquivo="turmas")
        dados[identificador] = informacoes
        criptografar_json(dados=dados, arquivo="turmas")
        return [2, "Turma cadastrada."]


def get_turma(identificador):
    """Espera receber o identificador do turma e retorna suas informações

    Args:
        identificador (str): Identificador geral do turma

    Returns:
        dict: Informações do turma
    """
    dados = descriptografar_json("turmas")
    print(dados)
    if not identificador in dados:
        print("Turma não localizado no sistema.")
        return None
    else:
        return {"nome": identificador, **dados[identificador]}


def editar_turma(turma: dict) -> str:
    """Recebe um dicionário com os dados da turma e atualiza o arquivo JSON.

    Args:
        usuario (dict): Informações da turma

    Returns:
        str: Informativo do status da operação
    """
    dados = descriptografar_json(arquivo="turmas")
    for identificador, informacoes in turma.items():
        break
    dados[identificador] = informacoes
    criptografar_json(dados=dados, arquivo="turmas")
    return f"Turma atualizada."
