import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from datetime import datetime
from dados import get_turma, editar_turma
from telas.utils_tk import limpar_widgets
import contexto
from config import GUI_FONT

TECLAS_IGNORADAS = ("BackSpace", "Delete", "Left", "Up", "Down", "Right", "Return")


def atualizar_dados():
    turma = {}
    turma[dados_turma["nome"].get()] = {
        "curso": dados_turma["curso"].get(),
        "periodo": dados_turma["periodo"].get(),
        "criador": dados_turma["criador"],
        "frequencia": dados_turma["frequencia"],
    }
    status = editar_turma(turma)
    # Mostra a mensagem antes de limpar o frame para não usar um parent destruído
    messagebox.showinfo(
        "Edição", message=status, icon="info", parent=frame_edicao_turma
    )
    limpar_widgets(frame_edicao_turma)


def reconstruir_frame(turma_buscada):
    global frame_edicao_turma
    global dados_turma

    frame_edicao_turma = tk.Frame(contexto.frame_conteudo)

    for i in range(1, 10):
        frame_edicao_turma.rowconfigure(i, minsize=20)
    frame_edicao_turma.columnconfigure((0, 6), minsize=10)
    frame_edicao_turma.columnconfigure((1, 2, 3, 4, 5), pad=5, weight=0, minsize=10)
    frame_edicao_turma.grid(row=0, column=0, sticky="sew", pady=15)

    # Nome
    label_nome_turma = tk.Label(
        frame_edicao_turma, text="Nome da turma: ", font=(GUI_FONT, 16, "bold")
    )
    campo_nome_turma = tk.StringVar()
    entry_nome_turma = tk.Entry(
        frame_edicao_turma, textvariable=campo_nome_turma, font=(GUI_FONT, 16)
    )
    dados_turma["nome"] = campo_nome_turma
    entry_nome_turma.bind("<Return>", atualizar_dados)
    entry_nome_turma.focus()

    # Curso
    label_nome_curso = tk.Label(
        frame_edicao_turma, text="Curso: ", font=(GUI_FONT, 16, "bold")
    )
    campo_nome_curso = tk.StringVar()
    entry_nome_curso = tk.Entry(
        frame_edicao_turma, textvariable=campo_nome_curso, font=(GUI_FONT, 16)
    )
    dados_turma["curso"] = campo_nome_curso
    entry_nome_curso.bind("<Return>", atualizar_dados)

    # Período
    label_periodo = tk.Label(
        frame_edicao_turma, text="Período: ", font=(GUI_FONT, 16, "bold")
    )
    campo_periodo = tk.StringVar()
    combobox_periodo = ttk.Combobox(
        frame_edicao_turma, textvariable=campo_periodo, font=(GUI_FONT, 16)
    )
    combobox_periodo["values"] = ("Manhã", "Tarde", "Noite")
    dados_turma["periodo"] = campo_periodo

    # Criador
    dados_turma["criador"] = turma_buscada["criador"]

    # Frequência
    dados_turma["frequencia"] = turma_buscada["frequencia"]

    # Popular campos
    entry_nome_curso.insert(0, turma_buscada["curso"])
    entry_nome_turma.insert(0, turma_buscada["nome"])
    campo_periodo.set(turma_buscada["periodo"])

    # Botões
    botao_salvar = ttk.Button(
        frame_edicao_turma,
        text="Salvar",
        bootstyle="primary",
        command=atualizar_dados,
    )
    botao_cancelar = ttk.Button(
        frame_edicao_turma,
        text="Cancelar",
        bootstyle="primary-outline",
        command=lambda: limpar_widgets(),
    )

    # Row 0
    label_nome_curso.grid(row=0, column=0, pady=10, sticky="w")
    entry_nome_curso.grid(row=0, column=1, columnspan=2, ipadx=80, sticky="w")

    # Row 0
    label_nome_turma.grid(row=1, column=0, pady=10, sticky="w")
    entry_nome_turma.grid(row=1, column=1, columnspan=2, ipadx=80, sticky="w")

    # Row 1
    label_periodo.grid(row=2, column=0, pady=10, sticky="w")
    combobox_periodo.grid(row=2, column=1, sticky="w")

    # Row 8
    botao_cancelar.grid(row=8, column=4, sticky="es", ipady=10, padx=2)
    botao_salvar.grid(row=8, column=6, sticky="wes", ipady=10, padx=2)


dados_turma = {}


def interface_busca():
    global frame_busca_turma
    frame_busca_turma = tk.Frame(contexto.frame_conteudo)
    label_turma = tk.Label(
        frame_busca_turma,
        text="Digite o nome da turma para buscar:",
        font=(GUI_FONT, 16, "bold"),
    )
    campo_turma = tk.StringVar()
    entry_turma = tk.Entry(
        frame_busca_turma, textvariable=campo_turma, font=(GUI_FONT, 16)
    )
    dados_turma["nome"] = entry_turma
    entry_turma.bind(
        "<Return>",
        lambda event: buscar_turma(entry_turma.get(), event),
    )
    botao_buscar = ttk.Button(
        frame_busca_turma,
        text="Buscar",
        bootstyle="primary",
        command=lambda: buscar_turma(entry_turma.get()),
    )

    frame_busca_turma.grid()
    frame_busca_turma.columnconfigure((1, 2, 3, 4, 5), minsize=5)
    label_turma.grid(row=2, column=0, pady=10, sticky="w")
    entry_turma.grid(row=2, column=1, sticky="w")
    botao_buscar.grid(row=2, column=4, sticky="e")


def buscar_turma(nome, event=None):
    limpar_widgets()
    turma_buscada = get_turma(nome)
    if turma_buscada != None:
        reconstruir_frame(turma_buscada)
    else:
        messagebox.showinfo("Inválido.", message="Turma não localizada.")
        iniciar_edicao_turma()


def iniciar_edicao_turma():
    limpar_widgets()
    interface_busca()


if __name__ == "__main__":
    iniciar_edicao_turma()
