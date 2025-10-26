import os
from dotenv import get_key, set_key
from cryptography.fernet import Fernet
from paths import FILES_PATH
from argon2 import PasswordHasher, exceptions
from string import digits, ascii_letters
from random import randint
import pyperclip


def checar_existencia_env() -> None:
    if not os.path.exists(FILES_PATH + ".env"):
        string_key = Fernet.generate_key().decode()
        with open(FILES_PATH + ".env", "x") as file:
            file.write(
                f"ADMINISTRADOR=UNIP25ADS\nSECRET_KEY={string_key}\n\
EMAIL_PASSWORD='oucs ptcj esun ruoc'\n"
            )


def get_env_key(key: str) -> str:
    return get_key(FILES_PATH + ".env", key)


def set_env_key(key: str, value: str) -> str:
    return set_key(FILES_PATH + ".env", key, value)


def get_fernet():
    return Fernet(get_env_key("SECRET_KEY").encode())


def hashear_senha(senha):
    return ph.hash(senha)


def verificar_senha(hash, senha):
    try:
        ph.verify(hash, senha)
        return 0
    except exceptions.VerifyMismatchError:
        return 1


def gerar_senha_temp():
    char_len = len(ascii_letters + digits) - 1
    senha = "".join([(ascii_letters + digits)[randint(0, char_len)] for _ in range(8)])
    pyperclip.copy(senha)
    return senha


global ph
ph = PasswordHasher()
