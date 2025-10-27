import json
import os
from paths import FILES_PATH
from seguranca import get_fernet
import re

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


def descriptografar_json(arquivo):
    with open(FILES_PATH + FILE_NAMES[arquivo], mode="rb") as file:
        dados_protegidos = file.read()

        return json.loads(get_fernet().decrypt(dados_protegidos).decode())


def criptografar_json(dados, arquivo: str):
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


def get_aluno_by_cpf(cpf: str):
    """Espera receber o cpf do aluno e retorna suas informações

    Args:
        cpf (str): cpf do aluno

    Returns:
        dict: Informações do aluno
    """
    dados: dict = descriptografar_json("alunos")
    for ra, aluno in dados.items():
        if aluno["cpf"] == cpf:
            return {"ra": ra, **aluno}
    print("Usuário não localizado no sistema.")
    return None


def get_aluno_by_ra(ra: str):
    """Espera receber o RA do aluno e retorna suas informações

    Args:
        ra (str): RA do aluno

    Returns:
        dict: Informações do aluno
    """
    dados: dict = descriptografar_json("alunos")
    usuario: dict = dados.get(ra, None)
    if usuario == None:
        return None
    return {"ra": ra, **usuario}


def get_alunos_by_name(busca: str):
    """Espera receber o RA do aluno e retorna suas informações

    Args:
        ra (str): RA do aluno

    Returns:
        dict: Lista de ocorrências correspondentes a busca no formato {nome: ra,}
    """
    busca = busca.strip().split()
    padrao = ".*".join(map(re.escape, busca))
    regex = re.compile(padrao, re.IGNORECASE)
    # Obter lista de nomes de alunos
    dicionario_alunos = {}
    dados: dict = descriptografar_json("alunos")
    for ra, informacoes in dados.items():
        dicionario_alunos[informacoes["nome"]] = ra
    # Procurar nomes compatíveis
    nomes_compativeis = {
        nome: ra for nome, ra in dicionario_alunos.items() if regex.search(nome)
    }
    return nomes_compativeis


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
        criptografar_json(dados=dados, arquivo="colaboradores")
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


def add_aluno(aluno: dict) -> str:
    """Recebe um dicionário e verifica a por ocorrência no banco atual, formata devidamente e salva no JSON.

    Args:
        aluno (dict): Informações do aluno

    Returns:
        str: Informativo do status da operação
    """
    if not aluno:
        return [0, "Usuário inválido."]
    consulta = get_aluno_by_cpf(aluno["cpf"])
    if consulta != None:
        return [
            1,
            f"Aluno {aluno['nome']} já está cadastrado.",
        ]
    else:
        dados = descriptografar_json(arquivo="alunos")
        ra = get_next_ra()
        dados[ra] = aluno
        criptografar_json(dados=dados, arquivo="alunos")
        return [2, "Usuário cadastrado."]


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


def get_next_ra():
    dados: dict = descriptografar_json(arquivo="alunos")
    lista_ra = sorted([int(ra[2:]) for ra in dados.keys()])
    if not lista_ra:
        return "RA000"
    for i in range(len(lista_ra)):
        if i != lista_ra[i]:
            return "RA" + ((3 - len(str(i))) * "0") + str(i)
    return "RA" + ((3 - len(str(i))) * "0") + str(i + 1)
