import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from datetime import datetime
from dados import get_colaborador, editar_colaborador
from telas.utils_tk import limpar_widgets
import contexto
from seguranca import gerar_senha_temp, hashear_senha
from telas.utils_tk import (
    formatar_cpf,
    formatar_telefone,
    verificar_email,
    verificar_data,
)
from config import GUI_FONT

TECLAS_IGNORADAS = ("BackSpace", "Delete", "Left", "Up", "Down", "Right", "Return")


def atualizar_dados(event=None):
    # Limpa apenas a área de erros antes da validação
    limpar_widgets(frame_erros)
    usuario = {}
    erros = []
    cpf = "".join([digit for digit in dados_usuario["cpf"].get() if digit.isdigit()])
    if len(cpf) != 11:
        frame_edicao.label_cpf_invalido.config(text="CPF Inválido.")
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
    if not verificar_email(campo=dados_usuario["email"]):
        erros.append("- Email inválido.")
    if erros:
        for i in range(len(erros)):
            tk.Label(
                frame_erros, text=erros[i], fg="red", font=(GUI_FONT, 14, "bold")
            ).grid(row=i, column=0, sticky="w")
        return
    usuario = {
        "cpf": cpf,
        "nome": dados_usuario["nome"].get(),
        "nascimento": nascimento,
        "email": dados_usuario["email"].get(),
        "telefone": telefone,
        "cargo": dados_usuario["cargo"].get(),
        "senha": dados_usuario["senha"],
    }
    status = editar_colaborador(usuario)
    messagebox.showinfo("Cadastro", message=status, icon="info", parent=frame_edicao)
    limpar_widgets()


def resetar_senha(cpf):
    senha = gerar_senha_temp()
    mensagem_senha = f"Salve a senha do usuário: {senha}\nA senha foi copiada para a área de transferência."
    messagebox.showinfo(
        "Senha temporária", message=mensagem_senha, icon="info", parent=frame_edicao
    )
    # Pega direto do JSON os dados para não puxar das entrys da interface
    dados_usuario = get_colaborador(cpf)
    dados_usuario["senha"] = hashear_senha(senha)
    editar_colaborador(dados_usuario)


def reconstruir_frame(usuario_buscado):
    global frame_edicao, frame_erros
    global dados_usuario

    frame_edicao = tk.Frame(contexto.frame_conteudo)

    frame_edicao.rowconfigure((1, 2, 3, 4, 5, 6, 7), minsize=20)
    frame_edicao.rowconfigure(8, minsize=250, weight=1)
    frame_edicao.columnconfigure((0, 6), minsize=10)
    frame_edicao.columnconfigure((1, 2, 3, 4, 5), pad=5, weight=0, minsize=10)
    frame_edicao.grid(row=0, column=0, sticky="sew", pady=15)

    frame_erros = tk.Frame(frame_edicao, width=100, height=100)
    for i in range(6):
        frame_erros.rowconfigure(i, minsize=5, weight=1)
    frame_erros.grid(row=7, column=0, sticky="nw", columnspan=2)

    # Nome
    label_nome = tk.Label(frame_edicao, text="Nome: ", font=(GUI_FONT, 16, "bold"))
    campo_nome = tk.StringVar()
    entry_nome = tk.Entry(frame_edicao, textvariable=campo_nome, font=(GUI_FONT, 16))
    dados_usuario["nome"] = campo_nome
    entry_nome.bind("<Return>", atualizar_dados)

    # Data Nascimento
    label_nascimento = tk.Label(
        frame_edicao, text="Nascimento: ", font=(GUI_FONT, 16, "bold")
    )
    campo_nascimento = tk.StringVar()
    entry_nascimento = tk.Entry(
        frame_edicao, textvariable=campo_nascimento, font=(GUI_FONT, 16)
    )
    dados_usuario["nascimento"] = campo_nascimento
    entry_nascimento.bind("<Return>", atualizar_dados)
    entry_nascimento.bind(
        "<KeyPress>",
        lambda event: verificar_data(event, campo_nascimento, entry_nascimento),
    )

    # CPF
    label_cpf = tk.Label(frame_edicao, text="CPF: ", font=(GUI_FONT, 16, "bold"))
    campo_cpf = tk.StringVar()
    entry_cpf = tk.Entry(
        frame_edicao,
        textvariable=campo_cpf,
        font=(GUI_FONT, 16),
    )
    dados_usuario["cpf"] = campo_cpf
    entry_cpf.bind("<Return>", atualizar_dados)
    entry_cpf.bind(
        "<KeyPress>", lambda event: formatar_cpf(event, campo_cpf, entry_cpf)
    )

    # Email
    label_email = tk.Label(frame_edicao, text="E-mail: ", font=(GUI_FONT, 16, "bold"))
    campo_email = tk.StringVar()
    entry_email = tk.Entry(frame_edicao, textvariable=campo_email, font=(GUI_FONT, 16))
    dados_usuario["email"] = campo_email
    entry_email.bind("<Return>", atualizar_dados)
    entry_email.bind(
        "<KeyPress>", lambda event: verificar_email(campo_email, event, entry_email)
    )

    # Telefone
    label_telefone = tk.Label(
        frame_edicao, text="Telefone: ", font=(GUI_FONT, 16, "bold")
    )
    campo_telefone = tk.StringVar()
    entry_telefone = tk.Entry(
        frame_edicao, textvariable=campo_telefone, font=(GUI_FONT, 16)
    )
    dados_usuario["telefone"] = campo_telefone
    entry_telefone.bind("<Return>", atualizar_dados)
    entry_telefone.bind(
        "<KeyPress>",
        lambda event, campo=campo_telefone: formatar_telefone(
            event, campo, entry_telefone
        ),
    )

    # Cargo
    label_cargo = tk.Label(frame_edicao, text="Cargo: ", font=(GUI_FONT, 16, "bold"))
    campo_cargo = ttk.Combobox(
        frame_edicao, values=["Professor", "Coordenador"], font=(GUI_FONT, 14)
    )
    dados_usuario["cargo"] = campo_cargo

    # Popular campos
    entry_nome.insert(0, usuario_buscado["nome"])
    entry_cpf.insert(0, usuario_buscado["cpf"])
    entry_email.insert(0, usuario_buscado["email"])
    entry_nascimento.insert(0, usuario_buscado["nascimento"])
    entry_telefone.insert(0, usuario_buscado["telefone"])
    campo_cargo.set(usuario_buscado["cargo"])
    dados_usuario["senha"] = usuario_buscado["senha"]

    # Formatar
    formatar_cpf(event=None, campo=campo_cpf, entry=entry_cpf)
    entry_cpf.config(state="readonly")
    formatar_telefone(event=None, campo=campo_telefone, entry=entry_telefone)
    verificar_data(event=None, campo=campo_nascimento, entry=entry_nascimento)
    verificar_email(event=None, campo=campo_email, entry=entry_email)

    # Botões
    botao_resetar_senha = ttk.Button(
        frame_edicao,
        text="Gerar nova senha",
        bootstyle="primary-outline",
        command=lambda: resetar_senha(usuario_buscado["cpf"]),
    )
    botao_salvar = ttk.Button(
        frame_edicao,
        text="Salvar",
        bootstyle="primary",
        command=atualizar_dados,
    )
    botao_cancelar = ttk.Button(
        frame_edicao,
        text="Cancelar",
        bootstyle="primary-outline",
        command=lambda: limpar_widgets(),
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
    campo_cargo.grid(row=5, column=1, sticky="w", padx=5)

    # Row 8
    botao_cancelar.grid(row=8, column=4, sticky="es", ipady=10, padx=2)
    botao_resetar_senha.grid(row=8, column=5, sticky="wes", ipady=10, padx=2)
    botao_salvar.grid(row=8, column=6, sticky="wes", ipady=10, padx=2)


def interface_busca():
    global frame_busca_usuario
    frame_busca_usuario = tk.Frame(contexto.frame_conteudo)
    label_cpf = tk.Label(
        frame_busca_usuario,
        text="Digite o CPF do colaborador para buscar: ",
        font=(GUI_FONT, 16, "bold"),
    )
    campo_cpf = tk.StringVar()
    entry_cpf = tk.Entry(
        frame_busca_usuario, textvariable=campo_cpf, font=(GUI_FONT, 16)
    )
    entry_cpf.focus()
    dados_usuario["cpf"] = entry_cpf
    entry_cpf.bind(
        "<Return>",
        lambda event: buscar_colaborador(entry_cpf.get(), event),
    )
    entry_cpf.bind(
        "<KeyPress>", lambda event: formatar_cpf(event, campo_cpf, entry_cpf)
    )
    botao_buscar = ttk.Button(
        frame_busca_usuario,
        text="Buscar",
        bootstyle="primary",
        command=lambda: buscar_colaborador(entry_cpf.get()),
    )

    frame_busca_usuario.grid()
    frame_busca_usuario.columnconfigure((1, 2, 3, 4, 5), minsize=5)
    label_cpf.grid(row=2, column=0, pady=10, sticky="w")
    entry_cpf.grid(row=2, column=1, sticky="w")
    botao_buscar.grid(row=2, column=4, sticky="e")


def buscar_colaborador(cpf, event=None):
    limpar_widgets()
    cpf = "".join([digit for digit in cpf if digit.isdigit()])
    usuario_buscado = get_colaborador(cpf)
    if usuario_buscado != None:
        reconstruir_frame(usuario_buscado)
    else:
        messagebox.showinfo("Inválido.", message="CPF não localizado.")
        iniciar_edicao_colaborador()


def iniciar_edicao_colaborador():
    limpar_widgets()
    usuario_buscado = interface_busca()


dados_usuario = {}

if __name__ == "__main__":
    iniciar_edicao_colaborador()
