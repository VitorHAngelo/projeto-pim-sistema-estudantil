from dados import checar_json_existe, add_colaborador
from seguranca import checar_existencia_env
from login_interface import tela_login
import paths


def main():
    checar_existencia_env()
    checar_json_existe()
    tela_login()


if __name__ == "__main__":
    main()
