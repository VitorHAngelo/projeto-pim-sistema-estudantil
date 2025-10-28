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
from telas.interface_cadastro_aluno import iniciar_cadastro_aluno
from telas.interface_edicao_aluno import iniciar_edicao_aluno
from telas.utils_tk import alt_tamanho_janela


def criar_barra_admin(janela):
    barra_admin = tk.Menu(janela)
    janela.config(menu=barra_admin)
    alt_tamanho_janela(janela, 1300, 800)

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
    alt_tamanho_janela(janela, 1300, 800)

    # opcoes_menu_coordenador.add_separator()
    # Ações
    opcoes_menu_coordenador = tk.Menu(barra_coordenador, tearoff=0)
    opcoes_menu_coordenador.add_command(
        label="Alterar senha",
        command=lambda: alterar_senha_colaborador(frame_conteudo, colaborador),
    )
    opcoes_menu_coordenador.add_command(label="Logoff", command=logoff)

    barra_coordenador.add_cascade(label="Ações", menu=opcoes_menu_coordenador)

    # Turmas
    opcoes_menu_turma = tk.Menu(barra_coordenador, tearoff=0)
    opcoes_menu_turma.add_command(
        label="Nova turma",
        command=lambda: iniciar_cadastro_turma(frame_conteudo, colaborador["nome"]),
    )
    opcoes_menu_turma.add_command(
        label="Editar turma", command=lambda: iniciar_edicao_turma(frame_conteudo)
    )
    barra_coordenador.add_cascade(label="Turmas", menu=opcoes_menu_turma)

    # Alunos
    opcoes_menu_alunos = tk.Menu(barra_coordenador, tearoff=0)
    opcoes_menu_alunos.add_command(
        label="Adicionar Aluno",
        command=lambda: iniciar_cadastro_aluno(frame_conteudo),
    )
    opcoes_menu_alunos.add_command(
        label="Editar Aluno", command=lambda: iniciar_edicao_aluno(frame_conteudo)
    )
    barra_coordenador.add_cascade(label="Alunos", menu=opcoes_menu_alunos)
    return barra_coordenador


def criar_barra_professor(janela):
    barra_professor = tk.Menu(janela)
    janela.config(menu=barra_professor)
    alt_tamanho_janela(janela, 1300, 800)

    opcoes_menu_coordenador = tk.Menu(barra_professor, tearoff=0)
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

    barra_professor.add_cascade(label="Ações", menu=opcoes_menu_coordenador)

    return barra_professor


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
    if colaborador:
        janela.login_logo_frame.destroy()
        ui_geral(janela)
        if colaborador.get("login", None) == "Admin":
            criar_barra_admin(janela)
        elif colaborador.get("cargo", None) == "Coordenador":
            criar_barra_coordenador(janela)
        elif colaborador.get("cargo", None) == "Professor":
            criar_barra_professor(janela)


def main():
    global janela, frame_conteudo, colaborador
    checar_existencia_env()
    checar_json_existe()

    janela = tk.Tk()

    janela.protocol("WM_DELETE_WINDOW", lambda: encerrar(janela))
    janela.title("Sistema Estudantil")
    janela.iconbitmap(FILES_PATH + "SmartEdu.ico")
    alt_tamanho_janela(janela, 500, 500)
    janela.rowconfigure(0, weight=0, minsize=10)
    janela.rowconfigure(1, weight=0)
    janela.rowconfigure(2, weight=1)

    frame_conteudo = tk.Frame(janela)

    login()

    janela.mainloop()


if __name__ == "__main__":
    main()
