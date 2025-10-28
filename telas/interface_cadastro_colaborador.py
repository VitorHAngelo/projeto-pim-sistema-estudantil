import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from dados import get_colaborador, add_colaborador
from telas.utils_tk import limpar_widgets
from seguranca import hashear_senha, gerar_senha_temp
from config import GUI_FONT
from telas.utils_tk import (
    formatar_cpf,
    formatar_telefone,
    verificar_email,
    verificar_data,
)


def cadastrar():
    usuario = {}
    erros = []
    cpf = "".join([digit for digit in dados_usuario["cpf"].get() if digit.isdigit()])
    if len(cpf) != 11:
        frame_cadastro.label_cpf_invalido.config(text="CPF Inválido.")
        erros.append("- CPF Inválido.")
    telefone = "".join(
        [digit for digit in dados_usuario["telefone"].get() if digit.isdigit()]
    )
    if len(telefone) < 6:
        erros.append("- Telefone inválido.")
    nascimento = "".join(
        [digit for digit in dados_usuario["nascimento"].get() if digit.isdigit()]
    )
    if len(nascimento) < 8:
        erros.append("- Data de nascimento inválida.")
    if (
        not "@" in dados_usuario["email"].get()
        or not "." in dados_usuario["email"].get()
    ):
        erros.append("- Email inválido.")
    frame_erros = tk.Frame(frame_cadastro, width=100, height=100)
    for i in range(6):
        frame_erros.rowconfigure(i, minsize=5, weight=1)
    frame_erros.grid(row=7, column=0)
    if erros:
        for i in range(len(erros)):
            tk.Label(
                frame_erros, text=erros[i], fg="red", font=(GUI_FONT, 14, "bold")
            ).grid(row=i, column=0, sticky="w")
        return
    # Solicita nova senha temporária
    senha = gerar_senha_temp()
    # Cria dicionário com os dados recebidos da interface
    senha_crua = senha
    usuario[cpf] = {
        "nome": dados_usuario["nome"].get(),
        "nascimento": nascimento,
        "email": dados_usuario["email"].get(),
        "telefone": telefone,
        "cargo": dados_usuario["cargo"].get(),
        "senha": hashear_senha(senha),
    }
    status = add_colaborador(usuario)
    if status[0] in (1, 2):  # Se código for 1 ou 2
        limpar_widgets(frame_cadastro)
    status[1] = (
        status[1]
        + "\nSalve a senha do usuário: "
        + senha_crua
        + "\nA senha foi copiada para a área de transferência."
        if status[0] == 2
        else status[1]
    )
    messagebox.showinfo(
        "Cadastro", message=status[1], icon="info", parent=frame_cadastro
    )


def limpar():
    for widget in frame_cadastro.winfo_children():
        widget.destroy()


def cancelar():
    pass


def atalho_enter(event):
    if event.state in (40, 42, 262184, 262186) and event.keysym == "Return":
        cadastrar()


def reconstruir_frame(frame_conteudo):
    limpar_widgets(frame_conteudo)

    global frame_cadastro
    global dados_usuario

    frame_cadastro = tk.Frame(frame_conteudo)

    for i in range(1, 10):
        frame_cadastro.rowconfigure(i, minsize=20)
    # frame_cadastro.rowconfigure(8, minsize=250, weight=1)
    frame_cadastro.columnconfigure((0, 6), minsize=10)
    frame_cadastro.columnconfigure((1, 2, 3, 4, 5), pad=5, weight=0, minsize=10)
    frame_cadastro.grid(row=0, column=0, sticky="sew", pady=15)

    # Nome
    label_nome = tk.Label(frame_cadastro, text="Nome: ", font=(GUI_FONT, 16, "bold"))
    campo_nome = tk.StringVar()
    entry_nome = tk.Entry(frame_cadastro, textvariable=campo_nome, font=(GUI_FONT, 16))
    dados_usuario["nome"] = campo_nome
    entry_nome.bind("<KeyPress>", atalho_enter)
    entry_nome.focus()

    # Data Nascimento
    label_nascimento = tk.Label(
        frame_cadastro, text="Nascimento: ", font=(GUI_FONT, 16, "bold")
    )
    campo_nascimento = tk.StringVar()
    entry_nascimento = tk.Entry(
        frame_cadastro, textvariable=campo_nascimento, font=(GUI_FONT, 16)
    )
    dados_usuario["nascimento"] = campo_nascimento
    entry_nascimento.bind("<Return>", atalho_enter)
    entry_nascimento.bind(
        "<KeyPress>",
        lambda event: verificar_data(event, campo_nascimento, entry_nascimento),
    )

    # CPF
    label_cpf = tk.Label(frame_cadastro, text="CPF: ", font=(GUI_FONT, 16, "bold"))
    frame_cadastro.label_cpf_invalido = tk.Label(
        frame_cadastro,
        text="",
        font=(GUI_FONT, 16, "bold"),
        fg="red",
    )
    campo_cpf = tk.StringVar()
    entry_cpf = tk.Entry(frame_cadastro, textvariable=campo_cpf, font=(GUI_FONT, 16))
    dados_usuario["cpf"] = campo_cpf
    entry_cpf.bind("<Return>", atalho_enter)
    entry_cpf.bind(
        "<KeyPress>", lambda event: formatar_cpf(event, campo_cpf, entry_cpf)
    )

    # Email
    label_email = tk.Label(frame_cadastro, text="E-mail: ", font=(GUI_FONT, 16, "bold"))
    campo_email = tk.StringVar()
    entry_email = tk.Entry(
        frame_cadastro, textvariable=campo_email, font=(GUI_FONT, 16)
    )
    dados_usuario["email"] = campo_email
    entry_email.bind("<Return>", atalho_enter)
    entry_email.bind(
        "<KeyPress>", lambda event: verificar_email(event, campo_email, entry_email)
    )
    label_validacao_email = tk.Label(
        frame_cadastro, text="Digite um email válido.", font=(GUI_FONT, 12, "bold")
    )

    # Telefone
    label_telefone = tk.Label(
        frame_cadastro, text="Telefone: ", font=(GUI_FONT, 16, "bold")
    )
    campo_telefone = tk.StringVar()
    entry_telefone = tk.Entry(
        frame_cadastro, textvariable=campo_telefone, font=(GUI_FONT, 16)
    )
    dados_usuario["telefone"] = campo_telefone
    entry_telefone.bind("<Return>", atalho_enter)
    entry_telefone.bind(
        "<KeyPress>",
        lambda event, campo=campo_telefone: formatar_telefone(
            event, campo, entry_telefone
        ),
    )

    # Cargo
    label_cargo = tk.Label(frame_cadastro, text="Cargo: ", font=(GUI_FONT, 16, "bold"))
    cargos = [("Professor"), ("Coordenador")]
    campo_cargo = tk.StringVar()
    campo_cargo.set(1)
    dados_usuario["cargo"] = campo_cargo
    botoes_radio = []
    for i in range(2):
        botoes_radio.append(
            tk.Radiobutton(
                frame_cadastro,
                text=cargos[i],
                variable=campo_cargo,
                value=cargos[i],
                font=(GUI_FONT, 16),
            )
        )

    # Botões
    botao_salvar = tk.Button(
        frame_cadastro, text="Salvar", font=(GUI_FONT, 14, "bold"), command=cadastrar
    )
    botao_limpar = tk.Button(
        frame_cadastro, text="Limpar", font=(GUI_FONT, 14), command=limpar
    )
    botao_cancelar = tk.Button(
        frame_cadastro, text="Cancelar", font=(GUI_FONT, 14), command=cancelar
    )

    # Row 0
    label_nome.grid(row=1, column=0, pady=10, sticky="w")
    entry_nome.grid(row=1, column=1, columnspan=2, ipadx=80, sticky="w")
    label_nascimento.grid(row=1, column=3, sticky="e")
    entry_nascimento.grid(row=1, column=4, sticky="w")

    # Row 1
    label_cpf.grid(row=2, column=0, pady=10, sticky="w")
    entry_cpf.grid(row=2, column=1, sticky="w")
    label_email.grid(row=2, column=2, sticky="e")
    entry_email.grid(row=2, column=3, columnspan=2, sticky="we")

    # Row 2
    label_telefone.grid(row=3, column=0, pady=10, sticky="w")
    entry_telefone.grid(row=3, column=1, sticky="w")

    # Row 4
    label_cargo.grid(row=5, column=0, ipady=10, sticky="w")

    # Row 5
    for i in range(2):
        botoes_radio[i].grid(row=6, column=i, sticky="w", padx=5)

    # Row 8
    botao_cancelar.grid(row=8, column=4, sticky="es", ipady=10, padx=2)
    botao_limpar.grid(row=8, column=5, sticky="wes", ipady=10, padx=2)
    botao_salvar.grid(row=8, column=6, sticky="wes", ipady=10, padx=2)


dados_usuario = {}


def iniciar_cadastro(frame_conteudo):
    return reconstruir_frame(frame_conteudo)


if __name__ == "__main__":
    iniciar_cadastro()
