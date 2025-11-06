import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from telas.utils_tk import limpar_widgets
from dados import add_turma
from config import GUI_FONT
import contexto

TECLAS_IGNORADAS = ("BackSpace", "Delete", "Left", "Up", "Down", "Right", "Return")


def cadastrar():
    turma = {}
    erros = []
    if len(dados_turma["nome"].get()) < 4:
        erros.append("Nome inválido")
    if len(dados_turma["curso"].get()) < 3:
        erros.append("Curso inválido")
    frame_erros = tk.Frame(frame_cadastro_turma, width=100, height=100)
    for i in range(6):
        frame_erros.rowconfigure(i, minsize=5, weight=1)
    frame_erros.grid(row=7, column=0)
    if erros:
        for i in range(len(erros)):
            tk.Label(
                frame_erros, text=erros[i], fg="red", font=(GUI_FONT, 14, "bold")
            ).grid(row=i, column=0, sticky="w")
        return
    turma[dados_turma["nome"].get()] = {
        "curso": dados_turma["curso"].get(),
        "periodo": dados_turma["periodo"].get(),
        "criador": dados_turma["criador"],
        "alunos": [],
        "atividades": [],
    }
    status = add_turma(turma)
    if status[0] in (1, 2):  # Se código for 1 ou 2
        limpar_widgets(frame_cadastro_turma)
    messagebox.showinfo(
        "Cadastro", message=status[1], icon="info", parent=frame_cadastro_turma
    )


def limpar():
    for widget in frame_cadastro_turma.winfo_children():
        widget.destroy()


def cancelar():
    pass


def reconstruir_frame(nome_colaborador):
    limpar_widgets()

    global frame_cadastro_turma
    global dados_turma
    dados_turma["criador"] = nome_colaborador

    frame_cadastro_turma = tk.Frame(contexto.frame_conteudo)

    for i in range(1, 10):
        frame_cadastro_turma.rowconfigure(i, minsize=20)
    # frame_cadastro_turma.rowconfigure(8, minsize=250, weight=1)
    frame_cadastro_turma.columnconfigure((0, 6), minsize=10)
    frame_cadastro_turma.columnconfigure((1, 2, 3, 4, 5), pad=5, weight=0, minsize=10)
    frame_cadastro_turma.grid(row=0, column=0, sticky="sew", pady=15)

    # Nome
    label_nome_turma = tk.Label(
        frame_cadastro_turma, text="Nome da turma: ", font=(GUI_FONT, 16, "bold")
    )
    campo_nome_turma = tk.StringVar()
    entry_nome_turma = tk.Entry(
        frame_cadastro_turma, textvariable=campo_nome_turma, font=(GUI_FONT, 16)
    )
    dados_turma["nome"] = campo_nome_turma
    entry_nome_turma.bind("<Return>", lambda event: cadastrar())
    entry_nome_turma.focus()

    # Curso
    label_nome_curso = tk.Label(
        frame_cadastro_turma, text="Curso: ", font=(GUI_FONT, 16, "bold")
    )
    campo_nome_curso = tk.StringVar()
    entry_nome_curso = tk.Entry(
        frame_cadastro_turma, textvariable=campo_nome_curso, font=(GUI_FONT, 16)
    )
    dados_turma["curso"] = campo_nome_curso
    entry_nome_curso.bind("<Return>", lambda event: cadastrar())

    # Período
    label_periodo = tk.Label(
        frame_cadastro_turma, text="Período: ", font=(GUI_FONT, 16, "bold")
    )
    campo_periodo = tk.StringVar()
    combobox_periodo = ttk.Combobox(
        frame_cadastro_turma, textvariable=campo_periodo, font=(GUI_FONT, 16)
    )
    combobox_periodo["values"] = ("Manhã", "Tarde", "Noite")
    dados_turma["periodo"] = campo_periodo

    # Botões
    botao_salvar = ttk.Button(
        frame_cadastro_turma,
        text="Salvar",
        bootstyle="primary",
        command=cadastrar,
    )
    botao_limpar = ttk.Button(
        frame_cadastro_turma,
        text="Limpar",
        bootstyle="primary-outline",
        command=limpar,
    )
    botao_cancelar = ttk.Button(
        frame_cadastro_turma,
        text="Cancelar",
        bootstyle="primary-outline",
        command=cancelar,
    )

    # Row 0
    label_nome_turma.grid(row=0, column=0, pady=10, sticky="w")
    entry_nome_turma.grid(row=0, column=1, columnspan=2, ipadx=80, sticky="w")

    # Row 0
    label_nome_curso.grid(row=1, column=0, pady=10, sticky="w")
    entry_nome_curso.grid(row=1, column=1, columnspan=2, ipadx=80, sticky="w")

    # Row 1
    label_periodo.grid(row=2, column=0, pady=10, sticky="w")
    combobox_periodo.grid(row=2, column=1, sticky="w")

    # Row 8
    botao_cancelar.grid(row=8, column=4, sticky="es", ipady=10, padx=2)
    botao_limpar.grid(row=8, column=5, sticky="wes", ipady=10, padx=2)
    botao_salvar.grid(row=8, column=6, sticky="wes", ipady=10, padx=2)


dados_turma = {}


def iniciar_cadastro_turma(nome_colaborador):
    return reconstruir_frame(nome_colaborador)


if __name__ == "__main__":
    iniciar_cadastro_turma()
