import json
import os

USERS_FILE = "usuarios.json"
FILES_PATH = "./files/"


def checar_json_existe():
    if not USERS_FILE in os.listdir(FILES_PATH):  # Se não existir
        print("Criando database.")

        with open(FILES_PATH + USERS_FILE, mode="w") as file:  # Cria arquivo
            json.dump({}, file)

    else:
        print("Arquivo JSON presente.")
