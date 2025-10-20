import json
import os
from dotenv import get_key, set_key
from cryptography.fernet import Fernet
from paths import FILES_PATH


def checar_existencia_env() -> None:
    if not os.path.exists(FILES_PATH + ".env"):
        string_key = Fernet.generate_key().decode()
        with open(FILES_PATH + ".env", "x") as file:
            file.write(f"ADMINISTRADOR=UNIP25ADS\nSECRET_KEY={string_key}\n")


def get_env_key(key: str) -> str:
    return get_key(FILES_PATH + ".env", key)


def set_env_key(key: str, value: str) -> str:
    return set_key(FILES_PATH + ".env", key, value)


def get_fernet():
    return Fernet(get_env_key("SECRET_KEY").encode())
