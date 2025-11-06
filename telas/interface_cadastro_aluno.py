import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from dados import add_aluno, get_turmas
from telas.utils_tk import limpar_widgets
from telas.utils_tk import (
    formatar_cpf,
    formatar_telefone,
    verificar_email,
    verificar_data,
)
import contexto
from config import GUI_FONT

TECLAS_IGNORADAS = (
    "BackSpace",
    "Delete",
    "Left",
    "Up",
    "Down",
    "Right",
    "Return",
    "Home",
    "End",
)


def cadastrar(event=None):
    # Limpa apenas a área de erros antes da validação
    limpar_widgets(frame_erros)
    dados_aluno = {}
    erros = []
    # CPF
    cpf = "".join([digit for digit in aluno["cpf"].get() if digit.isdigit()])
    if len(cpf) != 11:
        frame_cadastro_aluno.label_cpf_invalido.config(text="CPF Inválido.")
        erros.append("- CPF Inválido.")
    # TELEFONE
    telefone = "".join([digit for digit in aluno["telefone"].get() if digit.isdigit()])
    # TELEFONE 2
    telefone_resp = "".join(
        [digit for digit in aluno["telefone_resp"].get() if digit.isdigit()]
    )
    if len(telefone) < 10 and len(telefone_resp) < 10:
        erros.append("- Pelo menos um telefone válido é necessário.")
    # NASCIMENTO
    nascimento = "".join(
        [digit for digit in aluno["nascimento"].get() if digit.isdigit()]
    )
    if len(nascimento) < 8:
        erros.append("- Data de nascimento inválida.")
    # EMAIL
    if not verificar_email(campo=aluno["email"]):
        erros.append("- Email inválido.")
    # TURMAS
    turma = aluno["turma"].get()
    if not turma in get_turmas() and turma:
        erros.append("- Turma inexistente.")
    if erros:
        for i in range(len(erros)):
            tk.Label(
                frame_erros, text=erros[i], fg="red", font=(GUI_FONT, 14, "bold")
            ).grid(row=i, column=0, sticky="w")
        return
    dados_aluno = {
        "nome": str(aluno["nome"].get()).title(),
        "cpf": cpf,
        "nascimento": nascimento,
        "email": str(aluno["email"].get()).lower(),
        "telefone": telefone,
        "telefone_resp": telefone_resp,
        "turma": turma if turma else None,
        "obs": aluno["obs"].get("1.0", "end-1c"),
        "notas": {},
    }
    status = add_aluno(dados_aluno)
    if status[0] in (1, 2):  # Se código for 1 ou 2
        limpar_widgets(frame_cadastro_aluno)
    messagebox.showinfo(
        "Cadastro", message=status[1], icon="info", parent=frame_cadastro_aluno
    )


def limpar():
    for widget in frame_cadastro_aluno.winfo_children():
        widget.destroy()


def cancelar():
    pass


def reconstruir_frame():
    limpar_widgets()

    global frame_cadastro_aluno, frame_erros
    global aluno

    frame_cadastro_aluno = tk.Frame(contexto.frame_conteudo)

    for i in range(1, 10):
        frame_cadastro_aluno.rowconfigure(i, minsize=20)
    frame_cadastro_aluno.columnconfigure((0, 6), minsize=10)
    frame_cadastro_aluno.columnconfigure((1, 2, 3, 4, 5), pad=5, weight=0, minsize=10)
    frame_cadastro_aluno.grid(row=0, column=0, sticky="sew", pady=15)

    frame_erros = tk.Frame(frame_cadastro_aluno, width=100, height=100)
    for i in range(6):
        frame_erros.rowconfigure(i, minsize=5, weight=1)
    frame_erros.grid(row=7, column=0, sticky="nw", columnspan=2)

    # Nome
    label_nome = tk.Label(
        frame_cadastro_aluno, text="Nome: ", font=(GUI_FONT, 16, "bold")
    )
    campo_nome = tk.StringVar()
    entry_nome = tk.Entry(
        frame_cadastro_aluno, textvariable=campo_nome, font=(GUI_FONT, 16)
    )
    aluno["nome"] = campo_nome
    entry_nome.bind("<Return>", cadastrar)
    entry_nome.focus()

    # Data Nascimento
    label_nascimento = tk.Label(
        frame_cadastro_aluno, text="Nascimento: ", font=(GUI_FONT, 16, "bold")
    )
    campo_nascimento = tk.StringVar()
    entry_nascimento = tk.Entry(
        frame_cadastro_aluno, textvariable=campo_nascimento, font=(GUI_FONT, 16)
    )
    aluno["nascimento"] = campo_nascimento
    entry_nascimento.bind("<Return>", cadastrar)
    entry_nascimento.bind(
        "<KeyPress>",
        lambda event: verificar_data(event, campo_nascimento, entry_nascimento),
    )

    # CPF
    label_cpf = tk.Label(
        frame_cadastro_aluno, text="CPF: ", font=(GUI_FONT, 16, "bold")
    )
    frame_cadastro_aluno.label_cpf_invalido = tk.Label(
        frame_cadastro_aluno,
        text="",
        font=(GUI_FONT, 16, "bold"),
        fg="red",
    )
    campo_cpf = tk.StringVar()
    entry_cpf = tk.Entry(
        frame_cadastro_aluno, textvariable=campo_cpf, font=(GUI_FONT, 16)
    )
    aluno["cpf"] = campo_cpf
    entry_cpf.bind("<Return>", cadastrar)
    entry_cpf.bind(
        "<KeyPress>", lambda event: formatar_cpf(event, campo_cpf, entry_cpf)
    )

    # Email
    label_email = tk.Label(
        frame_cadastro_aluno, text="E-mail: ", font=(GUI_FONT, 16, "bold")
    )
    campo_email = tk.StringVar()
    entry_email = tk.Entry(
        frame_cadastro_aluno, textvariable=campo_email, font=(GUI_FONT, 16)
    )
    aluno["email"] = campo_email
    entry_email.bind("<Return>", cadastrar)
    entry_email.bind(
        "<KeyPress>", lambda event: verificar_email(campo_email, event, entry_email)
    )
    label_validacao_email = tk.Label(
        frame_cadastro_aluno,
        text="Digite um email válido.",
        font=(GUI_FONT, 12, "bold"),
    )

    # Telefone
    label_telefone = tk.Label(
        frame_cadastro_aluno, text="Telefone: ", font=(GUI_FONT, 16, "bold")
    )
    campo_telefone = tk.StringVar()
    entry_telefone = tk.Entry(
        frame_cadastro_aluno, textvariable=campo_telefone, font=(GUI_FONT, 16)
    )
    aluno["telefone"] = campo_telefone
    entry_telefone.bind("<Return>", cadastrar)
    entry_telefone.bind(
        "<KeyPress>",
        lambda event: formatar_telefone(event, campo_telefone, entry_telefone),
    )

    # Telefone2
    label_telefone_resp = tk.Label(
        frame_cadastro_aluno, text="Telefone/Responsável: ", font=(GUI_FONT, 16, "bold")
    )
    campo_telefone_resp = tk.StringVar()
    entry_telefone_resp = tk.Entry(
        frame_cadastro_aluno, textvariable=campo_telefone_resp, font=(GUI_FONT, 16)
    )
    aluno["telefone_resp"] = campo_telefone_resp
    entry_telefone_resp.bind("<Return>", cadastrar)
    entry_telefone_resp.bind(
        "<KeyPress>",
        lambda event: formatar_telefone(
            event, campo_telefone_resp, entry_telefone_resp
        ),
    )

    # Turma
    label_turma = tk.Label(
        frame_cadastro_aluno, text="Turma: ", font=(GUI_FONT, 16, "bold")
    )
    campo_turma = ttk.Combobox(
        frame_cadastro_aluno, values=get_turmas(), font=(GUI_FONT, 14)
    )
    aluno["turma"] = campo_turma

    # Observacoes
    label_obs = tk.Label(
        frame_cadastro_aluno, text="Observações: ", font=(GUI_FONT, 16, "bold")
    )
    entry_obs = tk.Text(frame_cadastro_aluno, width=60, height=6, font=(GUI_FONT, 12))
    scrollbar = tk.Scrollbar(frame_cadastro_aluno, command=entry_obs.yview)
    aluno["obs"] = entry_obs
    entry_obs.config(yscrollcommand=scrollbar.set)

    # Botões
    botao_salvar = ttk.Button(
        frame_cadastro_aluno,
        text="Salvar",
        bootstyle="primary",
        command=cadastrar,
    )
    botao_limpar = ttk.Button(
        frame_cadastro_aluno,
        text="Limpar",
        bootstyle="primary-outline",
        command=limpar,
    )
    botao_cancelar = ttk.Button(
        frame_cadastro_aluno,
        text="Cancelar",
        bootstyle="primary-outline",
        command=cancelar,
    )

    # Row 1
    label_nome.grid(row=1, column=0, pady=10, sticky="w")
    entry_nome.grid(row=1, column=1, columnspan=2, ipadx=80, sticky="w")
    label_nascimento.grid(row=1, column=3, sticky="e")
    entry_nascimento.grid(row=1, column=4, sticky="w")

    # Row 2
    label_cpf.grid(row=2, column=0, pady=10, sticky="w")
    entry_cpf.grid(row=2, column=1, sticky="w")
    label_email.grid(row=2, column=2, sticky="e")
    entry_email.grid(row=2, column=3, columnspan=2, sticky="we")

    # Row 3
    label_telefone.grid(row=3, column=0, pady=10, sticky="w")
    entry_telefone.grid(row=3, column=1, sticky="w")
    label_telefone_resp.grid(row=3, column=3, pady=10, sticky="e")
    entry_telefone_resp.grid(row=3, column=4, sticky="w")

    # Row 4
    label_obs.grid(row=4, column=0, ipady=10, sticky="w")
    label_turma.grid(row=4, column=3, pady=10, sticky="e")
    campo_turma.grid(row=4, column=4, pady=10, sticky="w")
    entry_obs.grid(row=5, column=0, ipady=10, columnspan=3, sticky="w", padx=15)
    scrollbar.grid(row=5, column=2, sticky="nse")

    # Row 8
    botao_cancelar.grid(row=8, column=4, sticky="es", ipady=10, padx=2)
    botao_limpar.grid(row=8, column=5, sticky="wes", ipady=10, padx=2)
    botao_salvar.grid(row=8, column=6, sticky="wes", ipady=10, padx=2)


aluno = {}


def iniciar_cadastro_aluno():
    return reconstruir_frame()


if __name__ == "__main__":
    iniciar_cadastro_aluno()
