import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from dados import get_colaborador, editar_colaborador
from telas.utils_tk import limpar_widgets
from seguranca import gerar_senha_temp, hashear_senha


FONTE = "Calibri"
TECLAS_IGNORADAS = ("BackSpace", "Delete", "Left", "Up", "Down", "Right", "Return")


def atualizar_dados():
    usuario = {}
    cpf = "".join([digit for digit in dados_usuario["cpf"].get() if digit.isdigit()])
    telefone = "".join(
        [digit for digit in dados_usuario["telefone"].get() if digit.isdigit()]
    )
    nascimento = "".join(
        [digit for digit in dados_usuario["nascimento"].get() if digit.isdigit()]
    )
    usuario[cpf] = {
        "nome": dados_usuario["nome"].get(),
        "nascimento": nascimento,
        "email": dados_usuario["email"].get(),
        "telefone": telefone,
        "cargo": dados_usuario["cargo"].get(),
    }
    status = editar_colaborador(usuario)
    limpar_widgets(frame_edicao)
    messagebox.showinfo("Cadastro", message=status, icon="info", parent=frame_edicao)


def atalho_enter(event):
    if event.state in (40, 42, 262184, 262186) and event.keysym == "Return":
        atualizar_dados()


def formatar_telefone(event, campo_telefone, entry):
    telefone = list(campo_telefone.get())
    if event.state == 40 and event.keysym == "Tab":
        if len(telefone) == 11:
            telefone.insert(0, "(")
            telefone.insert(3, ")")
            telefone.insert(9, "-")
            entry.delete(0, tk.END)
            entry.insert(0, "".join(telefone))
        elif len(telefone) == 10:
            telefone.insert(0, "(")
            telefone.insert(3, ")")
            telefone.insert(8, "-")
            entry.delete(0, tk.END)
            entry.insert(0, "".join(telefone))


def formatar_cpf(event, campo, entry):
    if event.state in (40, 262184) and event.keysym in TECLAS_IGNORADAS:
        return
    cpf = [char for char in campo.get() if char.isdigit()]
    if len(cpf) >= 3:
        cpf.insert(3, ".")
    if len(cpf) >= 6:
        cpf.insert(7, ".")
    if len(cpf) >= 9:
        cpf.insert(11, "-")
    entry.delete(0, tk.END)
    entry.insert(0, "".join(cpf[:14]))


def formatar_email(event, campo, entry):
    email = list(campo.get())
    if not "@" in email or not "." in email or " " in email:
        entry.config(fg="red")
    else:
        entry.config(fg="black")


def formatar_data(event, campo, entry):
    if event.state in (40, 262184) and event.keysym in TECLAS_IGNORADAS:
        return
    data = [letter for letter in campo.get() if letter.isdigit()]
    if event.state == 40 and event.keysym == "Tab" and len(data) == 6:
        if int("".join(data[-2:])) <= int(str(datetime.now().year)[2:]):
            entry.insert(6, 20)
        else:
            entry.insert(6, 19)
        return
    if len(data) > 1:
        data.insert(2, "/")
    if len(data) > 4:
        data.insert(5, "/")
    entry.delete(0, tk.END)
    entry.insert(0, "".join(data[:10]))


def resetar_senha(cpf):
    senha = gerar_senha_temp()
    mensagem_senha = f"Salve a senha do usuário: {senha}\nA senha foi copiada para a área de transferência."
    messagebox.showinfo(
        "Senha temporária", message=mensagem_senha, icon="info", parent=frame_edicao
    )
    # Pega direto do JSON os dados para não puxar das entrys da interface
    dados_usuario = get_colaborador(cpf)
    dados_usuario["senha"] = hashear_senha(senha)
    print(dados_usuario)
    editar_colaborador(dados_usuario)


def reconstruir_frame(frame_conteudo, usuario_buscado):
    global frame_edicao
    global dados_usuario

    frame_edicao = tk.Frame(frame_conteudo)

    frame_edicao.rowconfigure((1, 2, 3, 4, 5, 6, 7), minsize=20)
    frame_edicao.rowconfigure(8, minsize=250, weight=1)
    frame_edicao.columnconfigure((0, 6), minsize=10)
    frame_edicao.columnconfigure((1, 2, 3, 4, 5), pad=5, weight=0, minsize=10)
    frame_edicao.grid(row=0, column=0, sticky="sew", pady=15)

    # Nome
    label_nome = tk.Label(frame_edicao, text="Nome: ", font=(FONTE, 16, "bold"))
    campo_nome = tk.StringVar()
    entry_nome = tk.Entry(frame_edicao, textvariable=campo_nome, font=(FONTE, 16))
    dados_usuario["nome"] = campo_nome
    entry_nome.bind("<KeyPress>", atalho_enter)

    # Data Nascimento
    label_nascimento = tk.Label(
        frame_edicao, text="Nascimento: ", font=(FONTE, 16, "bold")
    )
    campo_nascimento = tk.StringVar()
    entry_nascimento = tk.Entry(
        frame_edicao, textvariable=campo_nascimento, font=(FONTE, 16)
    )
    dados_usuario["nascimento"] = campo_nascimento
    entry_nascimento.bind("<Return>", atalho_enter)
    entry_nascimento.bind(
        "<KeyPress>",
        lambda event: formatar_data(event, campo_nascimento, entry_nascimento),
    )

    # CPF
    label_cpf = tk.Label(frame_edicao, text="CPF: ", font=(FONTE, 16, "bold"))
    campo_cpf = tk.StringVar()
    entry_cpf = tk.Entry(
        frame_edicao,
        textvariable=campo_cpf,
        font=(FONTE, 16),
    )
    dados_usuario["cpf"] = campo_cpf
    entry_cpf.bind("<Return>", atalho_enter)
    entry_cpf.bind(
        "<KeyPress>", lambda event: formatar_cpf(event, campo_cpf, entry_cpf)
    )

    # Email
    label_email = tk.Label(frame_edicao, text="E-mail: ", font=(FONTE, 16, "bold"))
    campo_email = tk.StringVar()
    entry_email = tk.Entry(frame_edicao, textvariable=campo_email, font=(FONTE, 16))
    dados_usuario["email"] = campo_email
    entry_email.bind("<Return>", atalho_enter)
    entry_email.bind(
        "<KeyPress>", lambda event: formatar_email(event, campo_email, entry_email)
    )

    # Telefone
    label_telefone = tk.Label(frame_edicao, text="Telefone: ", font=(FONTE, 16, "bold"))
    campo_telefone = tk.StringVar()
    entry_telefone = tk.Entry(
        frame_edicao, textvariable=campo_telefone, font=(FONTE, 16)
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
    label_cargo = tk.Label(frame_edicao, text="Cargo: ", font=(FONTE, 16, "bold"))
    campo_cargo = ttk.Combobox(
        frame_edicao, values=["Professor", "Coordenador"], font=(FONTE, 14)
    )

    # Popular campos
    entry_nome.insert(0, usuario_buscado["nome"])
    entry_cpf.insert(0, usuario_buscado["cpf"])
    entry_email.insert(0, usuario_buscado["email"])
    entry_nascimento.insert(0, usuario_buscado["nascimento"])
    entry_telefone.insert(0, usuario_buscado["telefone"])
    entry_cpf.config(state="readonly")
    campo_cargo.set(usuario_buscado["cargo"])

    # Botões
    botao_resetar_senha = tk.Button(
        frame_edicao,
        text="Gerar nova senha",
        font=(FONTE, 14),
        command=lambda: resetar_senha(usuario_buscado["cpf"]),
    )
    botao_salvar = tk.Button(
        frame_edicao, text="Salvar", font=(FONTE, 14, "bold"), command=atualizar_dados
    )
    botao_cancelar = tk.Button(
        frame_edicao,
        text="Cancelar",
        font=(FONTE, 14),
        command=lambda: limpar_widgets(frame_edicao),
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


dados_usuario = {}


def interface_busca(frame_conteudo):
    global frame_busca_usuario
    frame_busca_usuario = tk.Frame(frame_conteudo)
    label_cpf = tk.Label(
        frame_busca_usuario,
        text="Digite o CPF do colaborador para buscar: ",
        font=(FONTE, 16, "bold"),
    )
    campo_cpf = tk.StringVar()
    entry_cpf = tk.Entry(frame_busca_usuario, textvariable=campo_cpf, font=(FONTE, 16))
    dados_usuario["cpf"] = entry_cpf
    entry_cpf.bind(
        "<Return>",
        lambda event: buscar_colaborador(frame_conteudo, entry_cpf.get(), event),
    )
    entry_cpf.bind(
        "<KeyPress>", lambda event: formatar_cpf(event, campo_cpf, entry_cpf)
    )
    botao_buscar = tk.Button(
        frame_busca_usuario,
        text="Buscar",
        command=lambda: buscar_colaborador(frame_conteudo, entry_cpf.get()),
    )

    frame_busca_usuario.grid()
    frame_busca_usuario.columnconfigure((1, 2, 3, 4, 5), minsize=5)
    label_cpf.grid(row=2, column=0, pady=10, sticky="w")
    entry_cpf.grid(row=2, column=1, sticky="w")
    botao_buscar.grid(row=2, column=4, sticky="e")


def buscar_colaborador(frame_conteudo, cpf, event=None):
    limpar_widgets(frame_busca_usuario)
    cpf = "".join([digit for digit in cpf if digit.isdigit()])
    usuario_buscado = get_colaborador(cpf)
    if usuario_buscado != None:
        reconstruir_frame(frame_conteudo, usuario_buscado)
    else:
        messagebox.showinfo("Inválido.", message="CPF não localizado.")
        iniciar_edicao_colaborador(frame_conteudo)


def iniciar_edicao_colaborador(frame_conteudo):
    limpar_widgets(frame_conteudo)
    usuario_buscado = interface_busca(frame_conteudo)


if __name__ == "__main__":
    iniciar_edicao_colaborador()
