import tkinter as tk
from tkinter import messagebox

FONTE = "Calibri"


def login():
    campo_nome.delete(0, tk.END)
    campo_senha.delete(0, tk.END)
    # solicitar login


def sem_acesso():
    messagebox.showinfo(
        title="Solicitação de acesso",
        message="Para solicitar acesso, busque o superior responsável pela instituição.\nTelefone: (16) 0000-0000\nEmail: diretor@instituicao.edu.br",
    )


def encerrar():
    if messagebox.askyesno(title="Sair?", message="Tem certeza que deseja sair?"):
        janela_login.destroy()


def atalho_enter(event):
    if event.state in (40, 262184) and event.keysym == "Return":
        login()
        # campo_senha.get()
        # campo_nome.get()
        pass


janela_login = tk.Tk()

janela_login.geometry("500x500")
janela_login.title("Sistema Estudantil")

logo = tk.Label(
    janela_login,
    text="Logo",
    font=(FONTE, 18, "bold"),
)
bemvindo = tk.Label(
    janela_login,
    text="Bem vindo(a) ao Sistema Estudantil",
    font=(FONTE, 14),
)

etiqueta_nome = tk.Label(
    janela_login,
    text="Usuário: ",
    font=(FONTE, 12, "bold"),
)
nome = tk.StringVar()
campo_nome = tk.Entry(janela_login, textvariable=nome, font=(FONTE, 12))
campo_nome.bind("<KeyPress>", atalho_enter)

senha = tk.StringVar()
campo_senha = tk.Entry(
    janela_login,
    textvariable=senha,
    font=(FONTE, 12, ""),
    show="*",
)
campo_senha.bind("<KeyPress>", atalho_enter)

etiqueta_senha = tk.Label(janela_login, text="Senha: ", font=(FONTE, 12, "bold"))

botao_login = tk.Button(
    janela_login,
    text="Entrar",
    font=(FONTE, 10, "bold"),
    command=login,
)
botao_esqueci_senha = tk.Button(
    janela_login,
    text="Esqueci minha senha",
    font=(
        FONTE,
        8,
    ),
    border=0,
    foreground="blue",
)
botao_cadastrar = tk.Button(
    janela_login,
    text="Não possuo acesso.",
    font=(FONTE, 10),
    command=sem_acesso,
)
botao_sair = tk.Button(janela_login, text="Sair", font=(FONTE, 10), command=encerrar)

janela_login.columnconfigure((0, 4), weight=1)
janela_login.columnconfigure((1, 2, 3), weight=0)
janela_login.rowconfigure(0, weight=1)
janela_login.rowconfigure(tuple(range(1, 7)), weight=0, pad=5)
janela_login.rowconfigure(8, weight=1)

logo.grid(row=0, column=1, columnspan=3, rowspan=2, sticky="")
bemvindo.grid(row=2, column=1, columnspan=3)
etiqueta_nome.grid(row=3, column=1, sticky="w")
campo_nome.grid(row=3, column=2, columnspan=1, sticky="w", padx=0)
etiqueta_senha.grid(row=4, column=1, sticky="we")
campo_senha.grid(row=4, column=2, columnspan=2, sticky="w")

botao_esqueci_senha.grid(row=5, column=2, sticky="ne")
botao_login.grid(row=6, column=1, sticky="e")
botao_cadastrar.grid(row=6, column=2)
botao_sair.grid(row=6, column=3)


def tela_login():
    janela_login.mainloop()
