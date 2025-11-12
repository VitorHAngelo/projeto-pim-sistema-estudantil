"""Funções utilitárias de segurança e gestão de chaves do ambiente.

Este módulo provê helpers para:
- garantir que o arquivo `.env` exista com chaves mínimas;
- ler e escrever chaves do `.env` via dotenv;
- criar um objeto Fernet a partir da SECRET_KEY;
- gerar e hashear senhas temporárias.

As funções usam `FILES_PATH` (do módulo `paths`) para localizar o arquivo
.env e têm efeitos colaterais (criação de arquivo e cópia de senha para a
área de transferência).
"""

import os
from dotenv import get_key, set_key
from cryptography.fernet import Fernet
from paths import FILES_PATH
from argon2 import PasswordHasher, exceptions
from string import digits, ascii_letters
from random import randint
import pyperclip


def checar_existencia_env() -> None:
    """Garante que o arquivo de variáveis de ambiente exista.

    Se o arquivo `.env` não existir dentro de `FILES_PATH`, cria-o e grava
    valores padrão (ADMINISTRADOR, SECRET_KEY, EMAIL_PASSWORD e GEMINI_API_KEY).

    Não retorna valor, apenas cria o arquivo quando necessário.
    """
    if not os.path.exists(FILES_PATH + ".env"):
        string_key = Fernet.generate_key().decode()
        with open(FILES_PATH + ".env", "x") as file:
            file.write(
                f"ADMINISTRADOR=UNIP25ADS\nSECRET_KEY={string_key}\n\
EMAIL_PASSWORD='oucs ptcj esun ruoc'\n\
GEMINI_API_KEY=AIzaSyAzaRCiuTx8hSQpnkhnDhrCjNncrq5wxcA"
            )


def get_env_key(key: str) -> str:
    """Retorna o valor da chave `key` do arquivo `.env`.

    Parâmetros:
    - key: nome da variável a ser lida.

    Retorna a string com o valor da variável ou None se não existir.
    """
    return get_key(FILES_PATH + ".env", key)


def set_env_key(key: str, value: str) -> str:
    """Define/atualiza a chave `key` no arquivo `.env` com `value`.

    Retorna o novo valor escrito (ou o resultado de set_key do dotenv).
    """
    return set_key(FILES_PATH + ".env", key, value)


def get_fernet():
    """Cria e retorna um objeto Fernet configurado com a SECRET_KEY.

    Usa `get_env_key("SECRET_KEY")` para obter a chave e inicializa
    um `cryptography.fernet.Fernet` a partir dela.
    """
    return Fernet(get_env_key("SECRET_KEY").encode())


def hashear_senha(senha):
    """Gera um hash de senha usando Argon2.

    Recebe a senha em texto simples e retorna o hash (string) gerado por
    `argon2.PasswordHasher`.
    """
    return ph.hash(senha)


def verificar_senha(hash, senha):
    """Verifica se a `senha` corresponde ao `hash` informado.

    Retorna 0 quando a verificação é bem-sucedida, 1 em caso de falha.
    """
    try:
        ph.verify(hash, senha)
        return 0
    except exceptions.VerifyMismatchError:
        return 1


def gerar_senha_temp():
    """Gera uma senha temporária aleatória e copia para a área de transferência.

    A senha tem 8 caracteres escolhidos entre letras e dígitos. A senha é
    retornada e também colocada no clipboard via `pyperclip.copy`.
    """
    char_len = len(ascii_letters + digits) - 1
    senha = "".join([(ascii_letters + digits)[randint(0, char_len)] for _ in range(8)])
    pyperclip.copy(senha)
    return senha


global ph
ph = PasswordHasher()
