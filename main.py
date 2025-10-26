from dados import checar_json_existe
from seguranca import checar_existencia_env
from telas.interface_login import tela_login
from telas.interface_cadastro_colaborador import iniciar_cadastro
from telas.alterar_senha_admin import alterar_senha_admin
from telas.interface_edicao_colaborador import iniciar_edicao_colaborador
from telas.interface_edicao_turma import iniciar_edicao_turma
from telas.alterar_senha_colaborador import alterar_senha_colaborador
from telas.utils_tk import ui_login, ui_geral
import tkinter as tk
from config import FILES_PATH
from telas.interface_cadastro_turma import iniciar_cadastro_turma
from telas.utils_tk import encerrar


def criar_barra_admin(janela):
    barra_admin = tk.Menu(janela)
    janela.config(menu=barra_admin)

    opcoes_menu_admin = tk.Menu(barra_admin, tearoff=0)
    opcoes_menu_admin.add_command(
        label="Novo colaborador",
        command=lambda: iniciar_cadastro(frame_conteudo),
    )
    opcoes_menu_admin.add_command(
        label="Editar colaborador",
        command=lambda: iniciar_edicao_colaborador(frame_conteudo),
    )
    opcoes_menu_admin.add_separator()
    opcoes_menu_admin.add_command(
        label="Alterar senha Admin", command=lambda: alterar_senha_admin(frame_conteudo)
    )
    opcoes_menu_admin.add_command(label="Logoff", command=logoff)

    barra_admin.add_cascade(label="Ações", menu=opcoes_menu_admin)

    return barra_admin


def criar_barra_coordenador(janela):
    barra_coordenador = tk.Menu(janela)
    janela.config(menu=barra_coordenador)

    opcoes_menu_coordenador = tk.Menu(barra_coordenador, tearoff=0)
    opcoes_menu_coordenador.add_command(
        label="Nova turma",
        command=lambda: iniciar_cadastro_turma(frame_conteudo, colaborador["nome"]),
    )
    opcoes_menu_coordenador.add_command(
        label="Editar turma", command=lambda: iniciar_edicao_turma(frame_conteudo)
    )
    opcoes_menu_coordenador.add_separator()
    opcoes_menu_coordenador.add_command(
        label="Alterar senha",
        command=lambda: alterar_senha_colaborador(frame_conteudo, colaborador),
    )
    opcoes_menu_coordenador.add_command(label="Logoff", command=logoff)

    barra_coordenador.add_cascade(label="Ações", menu=opcoes_menu_coordenador)

    return barra_coordenador


def logoff():
    global colaborador
    colaborador = {}

    for widget in janela.winfo_children():
        widget.destroy()

    login()


def login():
    global frame_conteudo, colaborador
    ui_login(janela)

    colaborador = tela_login(janela)

    frame_conteudo = tk.Frame(janela)
    frame_conteudo.grid(row=2, column=0, sticky="nsew", padx=0)
    frame_conteudo.grid_propagate(True)
    janela.geometry("1300x800")
    if colaborador:
        janela.login_logo_frame.destroy()
        ui_geral(janela)
        if colaborador.get("login", None) == "Admin":
            criar_barra_admin(janela)
        elif colaborador.get("cargo", None) == "Coordenador":
            criar_barra_coordenador(janela)


def main():
    global janela, frame_conteudo, colaborador
    checar_existencia_env()
    checar_json_existe()

    janela = tk.Tk()

    janela.protocol("WM_DELETE_WINDOW", lambda: encerrar(janela))
    janela.geometry("500x500")
    janela.title("Sistema Estudantil")
    janela.iconbitmap(FILES_PATH + "SmartEdu.ico")

    janela.rowconfigure(0, weight=0, minsize=10)
    janela.rowconfigure(1, weight=0)
    janela.rowconfigure(2, weight=1)

    frame_conteudo = tk.Frame(janela)

    login()

    janela.mainloop()


if __name__ == "__main__":
    main()
