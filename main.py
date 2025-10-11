from login_interface import login
from dados import checar_json_existe


def main():
    print("Hello from projeto-pim-sistema-estudantil!")
    checar_json_existe()
    login()


if __name__ == "__main__":
    main()
