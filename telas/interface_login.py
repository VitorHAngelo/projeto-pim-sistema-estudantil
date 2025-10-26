import tkinter as tk
from tkinter import messagebox
from seguranca import get_env_key
from telas.utils_tk import encerrar
from dados import get_colaborador, editar_colaborador
from seguranca import verificar_senha, gerar_senha_temp, hashear_senha
from email_tools import novo_email

FONTE = "Calibri"


def realizar_login(janela):
    global perfil
    login = campo_login.get()
    senha = campo_senha.get()
    campo_login.delete(0, tk.END)
    campo_senha.delete(0, tk.END)
    if login == "Admin" and senha == get_env_key("ADMINISTRADOR"):
        frame_login.destroy()
        janela.concluido.set(True)
        perfil = {"login": "Admin"}
    else:
        colaborador = get_colaborador(login)
        if isinstance(colaborador, dict):
            status = verificar_senha(colaborador.get("senha"), senha)
            if status == 0:
                frame_login.destroy()
                janela.concluido.set(True)
                perfil = get_colaborador(login)
                return
        messagebox.showwarning("Login inválido.", "Credenciais inválidas.")


def sem_acesso():
    messagebox.showinfo(
        title="Solicitação de acesso",
        message="Para solicitar acesso, busque o superior responsável pela instituição.\nTelefone: (16) 0000-0000\nEmail: diretor@instituicao.edu.br",
    )


def encerrar(janela):
    if messagebox.askyesno(title="Sair?", message="Tem certeza que deseja sair?"):
        janela.concluido.set(True)
        janela.quit()
        janela.after(50, janela.destroy)


def limpar(janela):
    for widget in frame_login.winfo_children():
        widget.destroy()


def atalho_enter(event, janela):
    if event.state in (40, 262184, 42, 262186) and event.keysym == "Return":
        realizar_login(janela)


def esqueci_senha():
    cpf = campo_login.get()
    print(cpf)
    colaborador = get_colaborador(cpf)
    if isinstance(colaborador, dict):
        senha = gerar_senha_temp()
        mensagem_senha = f"Foi enviada uma senha ao email cadastrado\n\
Verifique a caixa de Spam.\nCaso tenha problemas, contate o responsável pela instituição."
        messagebox.showinfo(
            "Redefinição de senha.",
            message=mensagem_senha,
            icon="info",
            parent=frame_login,
        )
        novo_email(colaborador, senha)
        colaborador["senha"] = hashear_senha(senha)
        editar_colaborador(colaborador)
    else:
        messagebox.showinfo(
            "Usuário inválido",
            message="Usuário não encontrado, por favor, digite um login válido.",
            icon="info",
            parent=frame_login,
        )


def reconstruir_login(janela):
    global campo_login, campo_senha, concluido, perfil, frame_login

    frame_login = tk.Frame(janela, pady=0)

    frame_login.grid(padx=100)

    bemvindo = tk.Label(
        frame_login,
        text="Bem vindo(a) ao Sistema Estudantil",
        font=(FONTE, 14),
    )

    janela.concluido = tk.BooleanVar()

    etiqueta_login = tk.Label(
        frame_login,
        text="Login:",
        font=(FONTE, 12, "bold"),
    )
    login = tk.StringVar()
    campo_login = tk.Entry(frame_login, textvariable=login, font=(FONTE, 12))
    campo_login.bind("<KeyPress>", lambda event: atalho_enter(event, janela))

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
        command=lambda: realizar_login(janela),
    )
    botao_esqueci_senha = tk.Button(
        frame_login,
        text="Esqueci minha senha",
        font=(
            FONTE,
            8,
        ),
        command=esqueci_senha,
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
        command=lambda: encerrar(janela),
    )

    frame_login.columnconfigure((0, 4), weight=1)
    frame_login.columnconfigure((1, 2, 3), weight=0)
    frame_login.rowconfigure(0, weight=1)
    frame_login.rowconfigure(tuple(range(1, 7)), weight=0, pad=5)
    frame_login.rowconfigure(8, weight=1)

    bemvindo.grid(row=2, column=1, columnspan=3)
    etiqueta_login.grid(row=3, column=1, sticky="w")
    campo_login.grid(row=3, column=2, columnspan=1, sticky="w", padx=0)
    etiqueta_senha.grid(row=4, column=1, sticky="we")
    campo_senha.grid(row=4, column=2, columnspan=2, sticky="w")

    botao_esqueci_senha.grid(row=5, column=2, sticky="ne")
    botao_login.grid(row=6, column=1, sticky="e")
    botao_cadastrar.grid(row=6, column=2)
    botao_sair.grid(row=6, column=3)

    janela.protocol("WM_DELETE_WINDOW", lambda: encerrar(janela))
    janela.wait_variable(janela.concluido)

    return perfil


def tela_login(janela):
    return reconstruir_login(janela)


perfil = {None: None}

if __name__ == "__main__":
    tela_login()
