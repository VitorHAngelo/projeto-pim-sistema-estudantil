from dados import checar_json_existe, add_colaborador
from seguranca import checar_existencia_env
from telas.interface_login import tela_login
from telas.interface_cadastro import iniciar_cadastro
from telas.alterar_senha_admin import alterar_senha
from telas.interface_edicao import iniciar_edicao
from telas.utils_tk import ui_login, ui_geral
import tkinter as tk
from config import FILES_PATH


def criar_barra_admin(janela):
    barra_admin = tk.Menu(janela)
    janela.config(menu=barra_admin)

    opcoes_menu_admin = tk.Menu(barra_admin, tearoff=0)
    opcoes_menu_admin.add_command(
        label="Novo colaborador",
        command=lambda: iniciar_cadastro(frame_conteudo),
    )
    opcoes_menu_admin.add_command(
        label="Editar colaborador", command=lambda: iniciar_edicao(frame_conteudo)
    )
    opcoes_menu_admin.add_separator()
    opcoes_menu_admin.add_command(
        label="Alterar senha Admin", command=lambda: alterar_senha(frame_conteudo)
    )
    opcoes_menu_admin.add_command(label="Logoff", command=logoff)

    barra_admin.add_cascade(label="Ações", menu=opcoes_menu_admin)

    return barra_admin


def logoff():
    global usuario
    usuario = {}

    main()


def main():
    global janela, frame_conteudo, usuario
    checar_existencia_env()
    checar_json_existe()

    janela = tk.Tk()

    janela.geometry("500x500")
    janela.title("Sistema Estudantil")
    janela.iconbitmap(FILES_PATH + "SmartEdu.ico")

    janela.rowconfigure(0, weight=0, minsize=10)
    janela.rowconfigure(1, weight=0)
    janela.rowconfigure(2, weight=1)

    frame_conteudo = tk.Frame(janela)

    # # ui_login(janela)

    # ## usuario = tela_login(janela)
    # ## if usuario:
    # ui_geral(janela)
    # ## if usuario.get("nome", None) == "Admin":
    # criar_barra_admin(janela)

    # -------------

    ui_login(janela)

    usuario = tela_login(janela)

    frame_conteudo.grid(row=2, column=0, sticky="nsew", padx=0)
    frame_conteudo.grid_propagate(True)
    janela.geometry("1300x800")
    if usuario:
        janela.login_logo_frame.destroy()
        ui_geral(janela)
        if usuario.get("nome", None) == "Admin":
            criar_barra_admin(janela)

    janela.mainloop()


if __name__ == "__main__":
    main()
