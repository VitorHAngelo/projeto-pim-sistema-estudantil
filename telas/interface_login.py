import tkinter as tk
from tkinter import messagebox
from seguranca import get_env_key
from telas.utils_tk import fechar
from config import FILES_PATH

FONTE = "Calibri"


def login(janela):
    global perfil
    nome = campo_nome.get()
    senha = campo_senha.get()
    campo_nome.delete(0, tk.END)
    campo_senha.delete(0, tk.END)
    if nome == "Admin" and senha == get_env_key("ADMINISTRADOR"):
        frame_login.destroy()
        janela.concluido.set(True)
        perfil = {"nome": "Admin"}


def sem_acesso():
    messagebox.showinfo(
        title="Solicitação de acesso",
        message="Para solicitar acesso, busque o superior responsável pela instituição.\nTelefone: (16) 0000-0000\nEmail: diretor@instituicao.edu.br",
    )


def encerrar(janela):
    if messagebox.askyesno(title="Sair?", message="Tem certeza que deseja sair?"):
        janela.destroy()


def limpar(janela):
    for widget in frame_login.winfo_children():
        widget.destroy()


def atalho_enter(event, janela):
    if event.state in (40, 262184, 42, 262186) and event.keysym == "Return":
        login(janela)


def reconstruir_login(janela):
    global campo_nome, campo_senha, concluido, perfil, frame_login

    frame_login = tk.Frame(janela, pady=0)

    frame_login.grid(padx=100)

    bemvindo = tk.Label(
        frame_login,
        text="Bem vindo(a) ao Sistema Estudantil",
        font=(FONTE, 14),
    )

    janela.concluido = tk.BooleanVar()

    etiqueta_nome = tk.Label(
        frame_login,
        text="Usuário: ",
        font=(FONTE, 12, "bold"),
    )
    nome = tk.StringVar()
    campo_nome = tk.Entry(frame_login, textvariable=nome, font=(FONTE, 12))
    campo_nome.bind("<KeyPress>", lambda event: atalho_enter(event, janela))

    senha = tk.StringVar()
    campo_senha = tk.Entry(
        frame_login,
        textvariable=senha,
        font=(FONTE, 12, ""),
        show="*",
    )
    campo_senha.bind("<KeyPress>", lambda event: atalho_enter(event, janela))

    etiqueta_senha = tk.Label(frame_login, text="Senha: ", font=(FONTE, 12, "bold"))

    botao_login = tk.Button(
        frame_login,
        text="Entrar",
        font=(FONTE, 10, "bold"),
        command=lambda: login(janela),
    )
    botao_esqueci_senha = tk.Button(
        frame_login,
        text="Esqueci minha senha",
        font=(
            FONTE,
            8,
        ),
        border=0,
        foreground="blue",
    )
    botao_cadastrar = tk.Button(
        frame_login,
        text="Não possuo acesso.",
        font=(FONTE, 10),
        command=sem_acesso,
    )
    botao_sair = tk.Button(
        frame_login,
        text="Sair",
        font=(FONTE, 10),
        command=lambda event: encerrar(event, frame_login),
    )

    frame_login.columnconfigure((0, 4), weight=1)
    frame_login.columnconfigure((1, 2, 3), weight=0)
    frame_login.rowconfigure(0, weight=1)
    frame_login.rowconfigure(tuple(range(1, 7)), weight=0, pad=5)
    frame_login.rowconfigure(8, weight=1)

    bemvindo.grid(row=2, column=1, columnspan=3)
    etiqueta_nome.grid(row=3, column=1, sticky="w")
    campo_nome.grid(row=3, column=2, columnspan=1, sticky="w", padx=0)
    etiqueta_senha.grid(row=4, column=1, sticky="we")
    campo_senha.grid(row=4, column=2, columnspan=2, sticky="w")

    botao_esqueci_senha.grid(row=5, column=2, sticky="ne")
    botao_login.grid(row=6, column=1, sticky="e")
    botao_cadastrar.grid(row=6, column=2)
    botao_sair.grid(row=6, column=3)

    janela.protocol("WM_DELETE_WINDOW", lambda: fechar(janela))
    janela.wait_variable(janela.concluido)

    return perfil


def tela_login(janela):
    return reconstruir_login(janela)


perfil = {None: None}

if __name__ == "__main__":
    tela_login()
