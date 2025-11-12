import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from config import FILES_PATH, GUI_FONT
from .utils_tk import limpar_widgets, TECLAS_IGNORADAS
import contexto
from dados import (
    get_turmas,
    get_atividades,
    get_turma,
    editar_turma,
    excluir_atividade,
    get_colaborador,
    editar_colaborador,
    get_alunos_turma,
    editar_aluno,
    get_aluno_by_ra,
)
from datetime import datetime
import calendar


def listar_atividades(frame, turma):
    limpar_widgets(frame_listagem)
    limpar_widgets(frame_editar_atividades)
    atividades = get_atividades(turma)
    cronograma = {"antigas": [], "atual": [], "futuras": []}
    for item in atividades:
        data = datetime.strptime(item["fim"], "%d%m%Y").date()
        hoje = datetime.today().date()

        if data < hoje:
            cronograma["antigas"].append(item)
        elif (data.month, data.year) == (hoje.month, hoje.year):
            cronograma["atual"].append(item)
        else:
            cronograma["futuras"].append(item)
    tk.Label(frame_listagem, text="Nome", font=(GUI_FONT, 14, "bold")).grid(
        row=0, column=0
    )
    tk.Label(
        frame_listagem, text="Início da atividade", font=(GUI_FONT, 14, "bold")
    ).grid(row=0, column=1, padx=10)
    tk.Label(frame_listagem, text="Fim da atividade", font=(GUI_FONT, 14, "bold")).grid(
        row=0, column=2, padx=10
    )
    i = 3
    for chave, valor in cronograma.items():
        if not valor:
            continue
        match chave:
            case "antigas":
                tk.Label(
                    frame_listagem,
                    text="• Tarefas passadas:",
                    font=(GUI_FONT, 14, "bold"),
                ).grid(row=i, column=0, sticky="w", pady=10)
                i += 1
            case "atual":
                tk.Label(
                    frame_listagem, text="• Mês atual:", font=(GUI_FONT, 14, "bold")
                ).grid(row=i, column=0, sticky="w", pady=10)
                i += 1
            case "futuras":
                tk.Label(
                    frame_listagem,
                    text="• Tarefas futuras:",
                    font=(GUI_FONT, 14, "bold"),
                ).grid(row=i, column=0, sticky="w", pady=10)
                i += 1
        for item in valor:
            tk.Label(frame_listagem, text=item["nome"], font=(GUI_FONT, 14)).grid(
                row=i, column=0
            )
            data = list(item["inicio"])
            data.insert(2, "/")
            data.insert(5, "/")
            data = "".join(data)
            tk.Label(frame_listagem, text=data, font=(GUI_FONT, 14)).grid(
                row=i, column=1
            )
            data = datetime.strptime(item["fim"], "%d%m%Y").date()
            antiga = False
            if data < hoje:
                antiga = True
            data = list(item["fim"])
            data.insert(2, "/")
            data.insert(5, "/")
            data = "".join(data)
            data_fim = tk.Label(frame_listagem, text=data, font=(GUI_FONT, 14))
            if antiga:
                data_fim.config(fg="red")
            data_fim.grid(row=i, column=2)
            edit = tk.PhotoImage(file=FILES_PATH + "pen.png")
            edit_label = tk.Label(frame_listagem, image=edit)
            edit_label.image = edit
            trash = tk.PhotoImage(file=FILES_PATH + "trash.png")
            trash_label = tk.Label(frame_listagem, image=trash)
            trash_label.image = trash
            test = tk.PhotoImage(file=FILES_PATH + "test.png")
            test_label = tk.Label(frame_listagem, image=test)
            test_label.image = test
            ttk.Button(
                frame_listagem,
                image=edit,
                command=lambda nome=item["nome"]: editar_atividade(nome, turma),
                bootstyle="primary-outline",
            ).grid(row=i, column=3)
            ttk.Button(
                frame_listagem,
                image=trash,
                command=lambda nome=item["nome"]: aviso_exclusao(nome, turma),
                bootstyle="primary-outline",
            ).grid(row=i, column=4)
            ttk.Button(
                frame_listagem,
                image=test,
                command=lambda nome=item["nome"]: interface_notas(nome),
                bootstyle="primary-outline",
            ).grid(row=i, column=5)
            i += 1


def aviso_exclusao(nome, turma):
    if messagebox.askyesno(
        "Excluir atividade?",
        message=f'Tem certeza que deseja excluir a atividade "{nome}"?',
        icon="warning",
    ):
        campo_turma.set("")
        limpar_widgets(frame_listagem)
        excluir_atividade(nome, turma)


def criar_interface_atividades():
    global frame_listagem, frame_editar_atividades, campo_turma

    limpar_widgets()
    frame_botoes = tk.Frame(contexto.frame_conteudo, height=50, width=300)
    frame_botoes.grid(row=0, column=0, sticky="nw")

    plus = tk.PhotoImage(file=FILES_PATH + "pluss.png")
    plus_label = tk.Label(frame_botoes, image=plus)
    plus_label.image = plus
    botao_add = ttk.Button(
        frame_botoes,
        image=plus,
        command=lambda: criar_atividade(frame_editar_atividades, razao="add"),
        bootstyle="primary-link",
    )

    largura_tela = contexto.frame_conteudo.winfo_toplevel().winfo_screenwidth()
    frame_lista_atividades = tk.Frame(
        contexto.frame_conteudo,
        height=1000,
        width=largura_tela // 3,
    )
    frame_lista_atividades.grid(row=1, column=0, sticky="nw")
    frame_listagem = tk.Frame(frame_lista_atividades)
    frame_listagem.grid(row=2, column=0)

    frame_editar_atividades = tk.Frame(
        contexto.frame_conteudo, height=1000, width=largura_tela // 2
    )

    titulo_label = tk.Label(
        frame_botoes, text="Selecione uma turma:", font=(GUI_FONT, 16, "bold")
    )

    turmas = get_turmas()
    campo_turma = ttk.Combobox(frame_botoes, values=turmas, font=(GUI_FONT, 14))
    campo_turma.bind(
        "<<ComboboxSelected>>",
        lambda event: listar_atividades(frame_lista_atividades, campo_turma.get()),
    )

    frame_editar_atividades.grid(row=1, column=1, sticky="nw", padx=15)
    titulo_label.grid(row=1, column=2, sticky="w")
    campo_turma.grid(row=1, column=3, pady=(8, 15), padx=5, sticky="w")

    botao_add.grid(row=1, column=0, padx=5, pady=5)
    ttk.Separator(frame_botoes, orient=tk.VERTICAL, bootstyle="primary").grid(
        row=1, column=1, padx=5
    )
    # botao_remove.grid(row=1, column=1, padx=5, pady=5)


def salvar_atividade(atividade, event=None):
    # Clear any previous error messages but do NOT destroy the input widgets yet
    # (calling limpar_widgets() without args removes widgets referenced below and
    # causes _tkinter.TclError when we try to .get() from them).
    try:
        limpar_widgets(frame_erros)
    except Exception:
        # frame_erros may not exist yet; ignore in that case
        pass
    erros = []
    # NOME ATIVIDADE
    lista_atividades = get_atividades(atividade["turma"].get())
    for item in lista_atividades:
        if item["nome"] == atividade["nome"].get():
            erros.append("- Já existe uma atividade com este nome.")
            break
    # INICIO
    inicio: datetime = atividade["inicio"].get_date()
    inicio = inicio.strftime("%d%m%Y")
    inicio = "".join([digit for digit in inicio if digit.isdigit()])
    if len(inicio) < 8:
        erros.append("- Início da atividade inválida.")
    # FIM
    fim: datetime = atividade["fim"].get_date()
    fim = fim.strftime("%d%m%Y")
    fim = "".join([digit for digit in fim if digit.isdigit()])
    if len(fim) < 8:
        erros.append("- Fim da atividade inválida.")
    # TURMA
    turma = str(atividade["turma"].get()).upper()
    if turma not in atividade["turmas"]:
        erros.append("- Turma inválida.")
    if erros:
        for i in range(len(erros)):
            tk.Label(
                frame_erros, text=erros[i], fg="red", font=(GUI_FONT, 14, "bold")
            ).grid(row=i, column=0, sticky="w")
        return
    nova_atividade = {}
    nova_atividade = {
        "nome": atividade["nome"].get(),
        "inicio": inicio,
        "fim": fim,
        "descricao": atividade["descricao"].get("1.0", "end-1c"),
        "professor": atividade["professor"],
        "nota": atividade["nota"].get(),
    }
    dados_turma = get_turma(atividade["turma"].get())
    nome_turma = dados_turma.pop("nome")
    dados_turma["atividades"].append(nova_atividade)
    editar_turma({nome_turma: dados_turma})
    messagebox.showinfo(
        "Cadastro", message="Atividade criada", icon="info", parent=frame_pai
    )
    # Clear the turma selector shown in the main listing (if it exists)
    try:
        campo_turma.set("")
    except Exception:
        pass
    # Refresh / clear only the edit and listing frames
    try:
        limpar_widgets(frame_editar_atividades)
    except Exception:
        pass
    try:
        limpar_widgets(frame_listagem)
    except Exception:
        pass


def formatar_nota(event):
    if event.keysym not in TECLAS_IGNORADAS:
        entry = event.widget
        nota = entry.get()
        valor_formatado = "".join(
            [char for char in nota if char.isdigit() or char == "."]
        )
        try:
            if float(valor_formatado) > atividade["nota"]:
                entry.delete(0, tk.END)
                return
        except ValueError:
            entry.delete(0, tk.END)
            entry.insert(0, valor_formatado)
        else:
            entry.delete(0, tk.END)
            entry.insert(0, valor_formatado)


def interface_notas(nome_atividade):
    global atividade, dicionario_notas
    dicionario_notas = {}
    limpar_widgets(frame_editar_atividades)
    turma = campo_turma.get()
    alunos = get_alunos_turma(turma)
    atividades = get_atividades(turma)
    for item in atividades:
        if item["nome"] == nome_atividade:
            atividade = item
    frame_editar_atividades.columnconfigure(0, weight=1)
    ttk.Label(
        frame_editar_atividades,
        text=f"Notas | {turma} | {nome_atividade}",
        font=(GUI_FONT, 15, "bold"),
    ).grid(row=0, column=0, pady=20, columnspan=2)

    def configurar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas = ttk.Canvas(frame_editar_atividades, width=400, height=440)
    frame_editar_atividades.grid_rowconfigure(2, weight=1)
    frame_editar_atividades.grid_columnconfigure(0, weight=1)
    frame_alunos = ttk.Frame(canvas, relief="sunken", height=150)
    frame_alunos.grid_columnconfigure(0, minsize=70, weight=0)
    frame_alunos.grid_columnconfigure(1, minsize=75, weight=0)
    frame_alunos.grid_columnconfigure(2, minsize=4, weight=0)
    canvas.grid(row=2, column=0, columnspan=3, sticky="nsew")
    window = canvas.create_window((0, 0), window=frame_alunos, anchor="nw")

    scrollbar = ttk.Scrollbar(
        frame_editar_atividades, orient="vertical", command=canvas.yview
    )
    scrollbar.grid(row=2, column=3, sticky="nsw")
    canvas.configure(yscrollcommand=scrollbar.set)

    frame_alunos.bind("<Configure>", configurar_scroll)

    def configurar_canvas(event):
        try:
            canvas.itemconfig(window, width=event.width)
        except Exception:
            pass

    def _on_mousewheel(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind("<Configure>", configurar_canvas)

    ttk.Label(frame_alunos, text="RA", font=(GUI_FONT, 14, "bold")).grid(
        row=1, column=0, padx=5, pady=8
    )
    ttk.Label(frame_alunos, text="Nome", font=(GUI_FONT, 14, "bold")).grid(
        row=1, column=1, padx=(5, 20), pady=8
    )
    ttk.Label(frame_alunos, text="Nota", font=(GUI_FONT, 14, "bold")).grid(
        row=1, column=2, padx=5, pady=8
    )

    linha = 2
    for ra, informacoes in alunos.items():
        # RA
        tk.Label(frame_alunos, text=ra, font=(GUI_FONT, 14)).grid(
            row=linha, column=0, pady=6
        )
        # Nome
        nome = informacoes["nome"]
        tk.Label(frame_alunos, text=nome, font=(GUI_FONT, 14)).grid(
            row=linha, column=1, pady=6
        )
        # Nota
        entry_nota = ttk.Entry(
            frame_alunos, bootstyle="primary", font=(GUI_FONT, 14), width=4
        )
        entry_nota.bind("<Tab>", formatar_nota)
        entry_nota.grid(row=linha, column=2, pady=3, padx=(5, 0))
        dicionario_notas[ra] = entry_nota
        linha += 1

        # Popular nota (se já existente)
        entry_nota.insert(0, informacoes["notas"].get(nome_atividade, ""))

    tk.Label(
        frame_editar_atividades,
        text=f"Nota máxima: {atividade['nota']}",
        font=(GUI_FONT, 14),
    ).grid(row=3, column=0, pady=6, padx=5)
    botao_cancelar = ttk.Button(
        frame_editar_atividades,
        text="Cancelar",
        bootstyle="primary-outline",
        command=lambda: limpar_widgets(frame_editar_atividades),
    )
    botao_salvar = ttk.Button(
        frame_editar_atividades,
        text="Salvar",
        bootstyle="primary",
        command=lambda: salvar_notas(dicionario_notas),  # ✔️
    )
    botao_cancelar.grid(row=3, column=1, pady=15, padx=5)
    botao_salvar.grid(row=3, column=2, pady=15)


def salvar_notas(dicionario_notas: dict):
    dicionario_preenchido = {}
    for ra, nota in dicionario_notas.items():
        if not nota.get():
            continue
        try:
            nota_float = float(nota.get())
            if nota_float > atividade["nota"] or nota_float < 0:
                messagebox.showerror("Nota inválida", "Nota fora dos limites impostos.")
                return
            dicionario_preenchido[ra] = nota_float
        except ValueError:
            messagebox.showerror("Nota inválida", "Favor, insira somente números.")
            return
    for ra, nota in dicionario_preenchido.items():
        aluno = get_aluno_by_ra(ra)
        aluno["notas"][atividade["nome"]] = nota
        editar_aluno(aluno)
    messagebox.showinfo(
        "Sucesso", f'Notas da atividade "{atividade['nome']}" atualizadas.'
    )


def salvar_edicao(atividade, nome_antigo):
    limpar_widgets(frame_erros)
    erros = []
    # NOME ATIVIDADE
    lista_atividades = get_atividades(atividade["turma"].get())
    for item in lista_atividades:
        if item["nome"] == atividade["nome"].get() and item["nome"] != nome_antigo:
            erros.append("- Já existe uma atividade com este nome.")
            break
    # INICIO
    inicio: datetime = atividade["inicio"].get_date()
    inicio = inicio.strftime("%d%m%Y")
    inicio = "".join([digit for digit in inicio if digit.isdigit()])
    if len(inicio) < 8:
        erros.append("- Início da atividade inválida.")
    # FIM
    fim: datetime = atividade["fim"].get_date()
    fim = fim.strftime("%d%m%Y")
    fim = "".join([digit for digit in fim if digit.isdigit()])
    if len(fim) < 8:
        erros.append("- Fim da atividade inválida.")
    # TURMA
    turma = str(atividade["turma"].get()).upper()
    if turma not in atividade["turmas"]:
        erros.append("- Turma inválida.")
    if erros:
        for i in range(len(erros)):
            tk.Label(
                frame_erros, text=erros[i], fg="red", font=(GUI_FONT, 14, "bold")
            ).grid(row=i, column=0, sticky="w")
        return
    atividade_atualizada = {}
    atividade_atualizada = {
        "nome": atividade["nome"].get(),
        "inicio": inicio,
        "fim": fim,
        "descricao": atividade["descricao"].get("1.0", "end-1c"),
        "professor": atividade["professor"],
        "nota": atividade["nota"].get(),
    }
    dados_turma = get_turma(atividade["turma"].get())
    nome_turma = dados_turma.pop("nome")
    for item in dados_turma["atividades"]:
        if item["nome"] == nome_antigo:
            dados_turma["atividades"].remove(item)
    dados_turma["atividades"].append(atividade_atualizada)
    editar_turma({nome_turma: dados_turma})
    messagebox.showinfo(
        "Cadastro", message="Atividade atualizada.", icon="info", parent=frame_pai
    )
    campo_turma.set("")
    limpar_widgets(frame_editar_atividades)
    limpar_widgets(frame_listagem)


def limpar(frame):
    # Limpa apenas o frame passado (não toda a janela), depois recria o formulário
    limpar_widgets(frame)
    criar_atividade(frame)


def criar_atividade(frame, razao=None):
    global nova_atividade, frame_erros
    nova_atividade = {}

    frame_erros = tk.Frame(frame, width=100, height=100)
    for i in range(6):
        frame_erros.rowconfigure(i, minsize=5, weight=1)
    frame_erros.grid(row=9, column=0, sticky="nw", columnspan=2, rowspan=4)

    titulo_label = tk.Label(frame, text="Criar atividade:", font=(GUI_FONT, 18, "bold"))
    # nome
    label_nome = tk.Label(frame, text="Nome: ", font=(GUI_FONT, 16, "bold"))
    campo_nome = tk.StringVar()
    entry_nome = tk.Entry(frame, textvariable=campo_nome, font=(GUI_FONT, 16))
    nova_atividade["nome"] = campo_nome
    entry_nome.bind("<Return>", lambda event: salvar_atividade(nova_atividade))
    entry_nome.focus()

    # data_inicio
    label_data_inicio = tk.Label(frame, text="Início: ", font=(GUI_FONT, 16, "bold"))
    calendario_inicio = ttk.DateEntry(
        frame_editar_atividades,
        dateformat="%d/%m/%Y",
        bootstyle="primary",
        startdate=datetime.today(),
    )
    nova_atividade["inicio"] = calendario_inicio

    # data_fim
    label_data_fim = tk.Label(frame, text="Fim: ", font=(GUI_FONT, 16, "bold"))
    calendario_fim = ttk.DateEntry(
        frame_editar_atividades,
        dateformat="%d/%m/%Y",
        bootstyle="primary",
        startdate=None,
    )
    nova_atividade["fim"] = calendario_fim

    # turma
    nova_atividade["turmas"] = get_turmas()
    label_turma = tk.Label(frame, text="Turma: ", font=(GUI_FONT, 16, "bold"))
    campo_turma = ttk.Combobox(
        frame, values=nova_atividade["turmas"], font=(GUI_FONT, 14)
    )
    nova_atividade["turma"] = campo_turma

    # nota
    label_nota = tk.Label(frame, text="Nota: ", font=(GUI_FONT, 16, "bold"))
    campo_nota = tk.DoubleVar()
    entry_nota = tk.Entry(frame, textvariable=campo_nota, font=(GUI_FONT, 16))
    campo_nota.set(10)
    nova_atividade["nota"] = campo_nota
    entry_nota.bind("<Return>", lambda event: salvar_atividade(nova_atividade))

    # descricao
    label_descricao = tk.Label(frame, text="Descrição: ", font=(GUI_FONT, 16, "bold"))
    entry_descricao = tk.Text(frame, width=42, height=6, font=(GUI_FONT, 12))
    scrollbar = tk.Scrollbar(frame, command=entry_descricao.yview)
    nova_atividade["descricao"] = entry_descricao
    entry_descricao.config(yscrollcommand=scrollbar.set)

    # docente
    nova_atividade["professor"] = contexto.colaborador["cpf"]

    botao_salvar = ttk.Button(
        frame,
        text="Salvar",
        bootstyle="primary",
        command=lambda: salvar_atividade(nova_atividade),
    )
    botao_limpar = ttk.Button(
        frame,
        text="Limpar",
        bootstyle="primary-outline",
        command=lambda: limpar(frame),
    )
    botao_cancelar = ttk.Button(
        frame,
        text="Cancelar",
        bootstyle="primary-outline",
        command=lambda: limpar_widgets(frame),
    )

    titulo_label.grid(row=0, column=0, sticky="w", columnspan=3)
    label_nome.grid(row=1, column=0, sticky="we")
    entry_nome.grid(row=1, column=1, columnspan=2, sticky="w")
    label_turma.grid(row=1, column=2, sticky="e", padx=15)
    campo_turma.grid(row=1, column=3, sticky="w", columnspan=4)

    label_data_inicio.grid(row=4, column=0, sticky="we")
    calendario_inicio.grid(row=4, column=1, sticky="w")
    label_data_fim.grid(row=5, column=0, sticky="we", padx=(20, 0))
    calendario_fim.grid(row=5, column=1, sticky="w")
    label_nota.grid(row=6, column=0, sticky="we")
    entry_nota.grid(row=6, column=1, sticky="w")
    label_descricao.grid(row=7, column=0, ipady=10, sticky="w")
    entry_descricao.grid(row=8, column=0, ipady=10, columnspan=5, sticky="w", padx=25)
    scrollbar.grid(row=8, column=0, sticky="nsw", padx=10)

    botao_cancelar.grid(row=9, column=3, pady=15, padx=5)
    botao_limpar.grid(row=9, column=4, pady=15, padx=5)
    botao_salvar.grid(row=9, column=5, pady=15, padx=5)


def editar_atividade(nome_atividade, turma):
    global atividade_edicao, frame_erros
    atividade_edicao = {}

    for item in get_atividades(turma):
        if item["nome"] == nome_atividade:
            atividade_salva = item
            break
    frame_erros = tk.Frame(frame_editar_atividades, width=100, height=100)
    for i in range(6):
        frame_erros.rowconfigure(i, minsize=5, weight=1)
    frame_erros.grid(row=9, column=0, sticky="nw", columnspan=2, rowspan=4)

    titulo_label = tk.Label(
        frame_editar_atividades, text="Editar atividade:", font=(GUI_FONT, 18, "bold")
    )

    # nome
    nome_antigo = atividade_salva["nome"]
    label_nome = tk.Label(
        frame_editar_atividades, text="Nome: ", font=(GUI_FONT, 16, "bold")
    )
    campo_nome = tk.StringVar()
    entry_nome = tk.Entry(
        frame_editar_atividades, textvariable=campo_nome, font=(GUI_FONT, 16)
    )
    atividade_edicao["nome"] = campo_nome
    entry_nome.bind("<Return>", lambda event: salvar_atividade(atividade_edicao))
    entry_nome.focus()

    # data_inicio
    label_data_inicio = tk.Label(
        frame_editar_atividades, text="Início: ", font=(GUI_FONT, 16, "bold")
    )
    calendario_inicio = ttk.DateEntry(
        frame_editar_atividades,
        dateformat="%d/%m/%Y",
        bootstyle="primary",
    )
    atividade_edicao["inicio"] = calendario_inicio

    # data_fim
    label_data_fim = tk.Label(
        frame_editar_atividades, text="Fim: ", font=(GUI_FONT, 16, "bold")
    )
    calendario_fim = ttk.DateEntry(
        frame_editar_atividades,
        dateformat="%d/%m/%Y",
        bootstyle="primary",
    )
    atividade_edicao["fim"] = calendario_fim

    # turma
    atividade_edicao["turmas"] = get_turmas()
    label_turma = tk.Label(
        frame_editar_atividades, text="Turma: ", font=(GUI_FONT, 16, "bold")
    )
    campo_turma = tk.StringVar()
    entry_turma = ttk.Entry(
        frame_editar_atividades, textvariable=campo_turma, font=(GUI_FONT, 14)
    )
    atividade_edicao["turma"] = campo_turma

    # nota
    label_nota = tk.Label(
        frame_editar_atividades, text="Nota: ", font=(GUI_FONT, 16, "bold")
    )
    campo_nota = tk.DoubleVar()
    entry_nota = tk.Entry(
        frame_editar_atividades, textvariable=campo_nota, font=(GUI_FONT, 16)
    )
    atividade_edicao["nota"] = campo_nota
    entry_nota.bind("<Return>", lambda event: salvar_atividade(atividade_edicao))

    # descricao
    label_descricao = tk.Label(
        frame_editar_atividades, text="Descrição: ", font=(GUI_FONT, 16, "bold")
    )
    entry_descricao = tk.Text(
        frame_editar_atividades, width=42, height=6, font=(GUI_FONT, 12)
    )
    scrollbar = tk.Scrollbar(
        frame_editar_atividades,
        command=entry_descricao.yview,
    )
    atividade_edicao["descricao"] = entry_descricao
    entry_descricao.config(yscrollcommand=scrollbar.set)

    # docente
    atividade_edicao["professor"] = contexto.colaborador["cpf"]

    # Popular campos
    entry_nome.insert(0, atividade_salva["nome"])
    inicio = datetime.strptime(atividade_salva["inicio"], "%d%m%Y").date()
    calendario_inicio.set_date(inicio)
    calendario_inicio.disable()
    fim = datetime.strptime(atividade_salva["fim"], "%d%m%Y").date()
    calendario_fim.set_date(fim)
    entry_turma.insert(0, turma)
    entry_turma.config(state="readonly")
    campo_nota.set(atividade_salva["nota"])
    entry_descricao.insert("1.0", atividade_salva["descricao"])

    botao_salvar = ttk.Button(
        frame_editar_atividades,
        text="Salvar",
        bootstyle="primary",
        command=lambda: salvar_edicao(atividade_edicao, nome_antigo),
    )
    botao_limpar = ttk.Button(
        frame_editar_atividades,
        text="Limpar",
        bootstyle="primary-outline",
        command=lambda: limpar(frame_editar_atividades),
    )
    botao_cancelar = ttk.Button(
        frame_editar_atividades,
        text="Cancelar",
        bootstyle="primary-outline",
        command=lambda: limpar_widgets(frame_editar_atividades),
    )

    titulo_label.grid(row=0, column=0, sticky="w", columnspan=3)
    label_nome.grid(row=1, column=0, sticky="we")
    entry_nome.grid(row=1, column=1, columnspan=2, sticky="w")
    label_turma.grid(row=1, column=2, sticky="e", padx=15)
    entry_turma.grid(row=1, column=3, sticky="w", columnspan=4)

    label_data_inicio.grid(row=4, column=0, sticky="we")
    calendario_inicio.grid(row=4, column=1, sticky="w")
    label_data_fim.grid(row=5, column=0, sticky="we", padx=(20, 0))
    calendario_fim.grid(row=5, column=1, sticky="w")
    label_nota.grid(row=6, column=0, sticky="we")
    entry_nota.grid(row=6, column=1, sticky="w")
    label_descricao.grid(row=7, column=0, ipady=10, sticky="w")
    entry_descricao.grid(row=8, column=0, ipady=10, columnspan=5, sticky="w", padx=25)
    scrollbar.grid(row=8, column=0, sticky="nsw", padx=10)

    botao_cancelar.grid(row=9, column=3, pady=15, padx=5)
    botao_limpar.grid(row=9, column=4, pady=15, padx=5)
    botao_salvar.grid(row=9, column=5, pady=15, padx=5)


def mudar_mes(mes: int, ano: int, operacao: str):
    if operacao == ">":
        mes += 1
    else:
        mes -= 1
    if mes > 12:
        ano += 1
        mes = mes % 12
    elif mes < 1:
        ano -= 1
        mes = 12
    criar_diario(mes, ano)


def criar_edicao_frequencia(data: datetime, turma):
    # Ensure the edit frame exists and is a valid widget. It may have been
    # destroyed by previous calls to limpar_widgets(contexto.frame_conteudo).
    global frame_editar_frequencia
    try:
        exists = frame_editar_frequencia.winfo_exists()
    except Exception:
        exists = False

    if not exists:
        # Recreate and grid the frame in the same place used by
        # criar_interface_frequencia so the UI remains consistent.
        frame_editar_frequencia = ttk.Frame(contexto.frame_conteudo)
        frame_editar_frequencia.grid(row=0, column=1, rowspan=10)

    limpar_widgets(frame_editar_frequencia)
    frame_editar_frequencia.columnconfigure(0, weight=1)
    ttk.Label(
        frame_editar_frequencia,
        text=f"Frequência | {turma} | {data.strftime('%d/%m/%Y')}",
        font=(GUI_FONT, 15, "bold"),
    ).grid(row=0, column=0, pady=20, columnspan=2)

    def configurar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas = ttk.Canvas(frame_editar_frequencia, width=400, height=440)
    frame_editar_frequencia.grid_rowconfigure(2, weight=1)
    frame_editar_frequencia.grid_columnconfigure(0, weight=1)
    frame_alunos = ttk.Frame(canvas, relief="sunken", height=150)
    frame_alunos.grid_columnconfigure(0, minsize=70, weight=0)
    frame_alunos.grid_columnconfigure(1, minsize=75, weight=0)
    frame_alunos.grid_columnconfigure(2, minsize=4, weight=0)
    canvas.grid(row=2, column=0, columnspan=3, sticky="nsew")
    window = canvas.create_window((0, 0), window=frame_alunos, anchor="nw")

    scrollbar = ttk.Scrollbar(
        frame_editar_frequencia, orient="vertical", command=canvas.yview
    )
    scrollbar.grid(row=2, column=3, sticky="nsw")
    canvas.configure(yscrollcommand=scrollbar.set)

    frame_alunos.bind("<Configure>", configurar_scroll)

    def configurar_canvas(event):
        try:
            canvas.itemconfig(window, width=event.width)
        except Exception:
            pass

    def _on_mousewheel(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind("<Configure>", configurar_canvas)

    alunos = get_alunos_turma(turma)

    ttk.Label(frame_alunos, text="RA", font=(GUI_FONT, 14, "bold")).grid(
        row=1, column=0, padx=5, pady=8
    )
    ttk.Label(frame_alunos, text="Nome", font=(GUI_FONT, 14, "bold")).grid(
        row=1, column=1, padx=(5, 20), pady=8
    )
    ttk.Label(frame_alunos, text="Presença", font=(GUI_FONT, 14, "bold")).grid(
        row=1, column=2, padx=5, pady=8
    )

    linha = 2
    dicionario_presenca = {}
    dados_turma = get_turma(turma)
    for ra, informacoes in alunos.items():
        # RA
        tk.Label(frame_alunos, text=ra, font=(GUI_FONT, 14)).grid(
            row=linha, column=0, pady=6
        )
        # Nome
        nome = informacoes["nome"]
        tk.Label(frame_alunos, text=nome, font=(GUI_FONT, 14)).grid(
            row=linha, column=1, pady=6
        )
        # Nota
        campo_presenca = tk.BooleanVar()
        toggle_presenca = ttk.Checkbutton(
            frame_alunos, bootstyle="primary-round-toggle", variable=campo_presenca
        )
        toggle_presenca.grid(row=linha, column=2, pady=3, padx=(5, 0))

        dados_chave = data.strftime("%d%m%Y")
        presente = dados_turma["frequencia"].get(dados_chave, {}).get(ra, False)

        campo_presenca.set(1 if presente else 0)
        dicionario_presenca[ra] = campo_presenca

        linha += 1

    def salvar_frequencia():
        # Get current turma data
        dados_turma = get_turma(turma)
        if not dados_turma:
            messagebox.showerror(
                "Erro",
                "Não foi possível encontrar os dados da turma para salvar frequência.",
            )
            return

        # Initialize frequency structure if it doesn't exist
        if "frequencia" not in dados_turma:
            dados_turma["frequencia"] = {}

        # Use date as key in ddmmyyyy format
        chave_data = data.strftime("%d%m%Y")
        if chave_data not in dados_turma["frequencia"]:
            dados_turma["frequencia"][chave_data] = {}

        # Update each student's attendance
        for ra, var in dicionario_presenca.items():
            dados_turma["frequencia"][chave_data][ra] = bool(var.get())

        # Save updated turma
        nome = dados_turma.pop("nome")  # editar_turma expects {nome: dados}
        if editar_turma({nome: dados_turma}):
            messagebox.showinfo(
                "Sucesso",
                "Frequência salva com sucesso!",
            )
            limpar_widgets(frame_editar_frequencia)
        else:
            messagebox.showerror(
                "Erro",
                "Erro ao salvar frequência. Tente novamente.",
            )

    botao_cancelar = ttk.Button(
        frame_editar_frequencia,
        text="Cancelar",
        bootstyle="primary-outline",
        command=lambda: limpar_widgets(frame_editar_frequencia),
    )
    botao_salvar = ttk.Button(
        frame_editar_frequencia,
        text="Salvar",
        bootstyle="primary",
        command=salvar_frequencia,  # ✔️
    )
    botao_cancelar.grid(row=3, column=1, pady=15, padx=5)
    botao_salvar.grid(row=3, column=2, pady=15)


def mudar_mes_frequencia(frame_calendario, mes: int, ano: int, operacao: str):
    # frame_calendario must be forwarded so gerar_calendario_frequencia
    # receives the correct widget (was passing ints previously)
    if operacao == ">":
        mes += 1
    else:
        mes -= 1
    if mes > 12:
        ano += 1
        mes = mes % 12
    elif mes < 1:
        ano -= 1
        mes = 12
    gerar_calendario_frequencia(frame_calendario, mes, ano)


def criar_diario(
    mes_escolhido=datetime.now().month,
    ano_escolhido=datetime.now().year,
):
    global frame_pai, frame_anotacoes
    frame_pai = contexto.frame_conteudo
    limpar_widgets()
    frame_barra_diario = ttk.Frame(contexto.frame_conteudo)
    frame_barra_diario.grid(row=0, column=0, padx=10, pady=10)

    botao_mes_anterior = ttk.Button(
        frame_barra_diario,
        text="<<",
        style="MenuButtons.Primary.TButton",
        command=lambda: mudar_mes(mes_escolhido, ano_escolhido, "<"),
    )
    data = datetime(ano_escolhido, mes_escolhido, 1)
    label_mes_ano = ttk.Label(
        frame_barra_diario,
        text=f"{data.strftime('%B').capitalize()} de {data.strftime('%Y')}",
        font=(GUI_FONT, 16, "bold"),
        width=16,
        anchor=tk.CENTER,
    )
    botao_mes_seguinte = ttk.Button(
        frame_barra_diario,
        text=">>",
        style="MenuButtons.Primary.TButton",
        command=lambda: mudar_mes(mes_escolhido, ano_escolhido, ">"),
    )
    botao_mes_anterior.grid(row=0, column=0, padx=5)
    # frame_barra_diario.columnconfigure(1, weight=1)
    label_mes_ano.grid(row=0, column=1, padx=5, sticky=tk.NSEW)
    botao_mes_seguinte.grid(row=0, column=2, padx=5)

    frame_diario = ttk.Frame(frame_barra_diario)
    frame_diario.grid(row=1, column=0, padx=10, pady=5, columnspan=10)
    # frame_diario.rowconfigure(1, weight=1)

    frame_anotacoes = ttk.Frame(frame_diario, relief="sunken", padding=10)
    frame_anotacoes.grid(row=0, column=9, padx=30, sticky="nwes", rowspan=30)
    frame_anotacoes.rowconfigure(10, weight=1)

    # Gerar cabeçalho calendário
    coluna = 0
    for letra_dia in "DSTQQSS":
        label_mes_ano = ttk.Label(
            frame_diario,
            text=letra_dia,
            font=(GUI_FONT, 14, "bold"),
            width=8,
            anchor=tk.CENTER,
        ).grid(row=0, column=coluna, sticky=tk.NSEW)
        coluna += 1
    dia_semana, qtd_dias = calendar.monthrange(ano_escolhido, mes_escolhido)
    dia_semana += 1

    linha = 1
    coluna = dia_semana
    for dia in range(1, qtd_dias + 1):
        if coluna > 6:
            coluna = coluna % 6
            coluna = coluna - 1
        data_impressa = f"{dia:02d}{mes_escolhido:02d}{ano_escolhido}"
        ttk.Button(
            frame_diario,
            text=dia,
            bootstyle="primary-outline",
            command=lambda data=data_impressa: editar_anotacoes(
                frame_anotacoes, datetime.strptime(data, "%d%m%Y"), contexto.colaborador
            ),
        ).grid(row=linha, column=coluna, ipady=6, padx=2, pady=2, sticky=tk.NSEW)
        if coluna == 6:
            linha += 1
        coluna += 1


def gerar_calendario_frequencia(
    mes_escolhido=datetime.now().month,
    ano_escolhido=datetime.now().year,
):
    limpar_widgets(frame_calendario)
    botao_mes_anterior = ttk.Button(
        frame_calendario,
        text="<<",
        style="MenuButtons.Primary.TButton",
        command=lambda: mudar_mes_frequencia(
            frame_calendario, mes_escolhido, ano_escolhido, "<"
        ),
    )
    data = datetime(ano_escolhido, mes_escolhido, 1)
    label_mes_ano = ttk.Label(
        frame_calendario,
        text=f"{data.strftime('%B').capitalize()} de {data.strftime('%Y')}",
        font=(GUI_FONT, 16, "bold"),
        width=16,
        anchor=tk.CENTER,
    )
    botao_mes_seguinte = ttk.Button(
        frame_calendario,
        text=">>",
        style="MenuButtons.Primary.TButton",
        command=lambda: mudar_mes_frequencia(
            frame_calendario, mes_escolhido, ano_escolhido, ">"
        ),
    )
    botao_mes_anterior.grid(row=0, column=0, padx=5)
    label_mes_ano.grid(row=0, column=1, padx=5, sticky=tk.NSEW, columnspan=3)
    botao_mes_seguinte.grid(row=0, column=4, padx=5)
    # Gerar cabeçalho calendário
    coluna = 0
    for letra_dia in "DSTQQSS":
        label_mes_ano = ttk.Label(
            frame_calendario,
            text=letra_dia,
            font=(GUI_FONT, 14, "bold"),
            width=8,
            anchor=tk.CENTER,
        ).grid(row=1, column=coluna, sticky=tk.NSEW)
        coluna += 1
    dia_semana, qtd_dias = calendar.monthrange(ano_escolhido, mes_escolhido)
    dia_semana += 1

    linha = 2
    coluna = dia_semana
    for dia in range(1, qtd_dias + 1):
        if coluna > 6:
            coluna = coluna % 6
            coluna = coluna - 1
        data_impressa = f"{dia:02d}{mes_escolhido:02d}{ano_escolhido}"
        ttk.Button(
            frame_calendario,
            text=dia,
            bootstyle="primary-outline",
            command=lambda data=data_impressa: criar_edicao_frequencia(
                datetime.strptime(data, "%d%m%Y"), campo_turma.get()
            ),
        ).grid(row=linha, column=coluna, ipady=6, padx=2, pady=2, sticky=tk.NSEW)
        if coluna == 6:
            linha += 1
        coluna += 1


def criar_interface_frequencia():
    global frame_editar_frequencia, frame_calendario, campo_turma
    limpar_widgets(contexto.frame_conteudo)
    frame_frequencia = ttk.Frame(contexto.frame_conteudo)
    frame_frequencia.grid(row=0, column=0)
    frame_escolha_turma = ttk.Frame(frame_frequencia)
    frame_escolha_turma.grid(row=0, column=0, padx=10, pady=10)
    frame_calendario = ttk.Frame(frame_frequencia)
    frame_calendario.grid(row=1, column=0, padx=10, pady=10)
    frame_editar_frequencia = ttk.Frame(contexto.frame_conteudo)
    frame_editar_frequencia.grid(row=0, column=1, rowspan=10)

    titulo_label = tk.Label(
        frame_escolha_turma, text="Selecione uma turma:", font=(GUI_FONT, 14, "bold")
    )

    turmas = get_turmas()
    campo_turma = ttk.Combobox(frame_escolha_turma, values=turmas, font=(GUI_FONT, 14))
    campo_turma.bind(
        "<<ComboboxSelected>>",
        lambda event: gerar_calendario_frequencia(),
    )
    titulo_label.grid(row=0, column=0, sticky="w")
    campo_turma.grid(row=0, column=1, pady=(8, 15), padx=5, sticky="w")

    frame_diario = ttk.Frame(frame_calendario)
    frame_diario.grid(row=1, column=0, padx=10, pady=5, columnspan=10)
    # frame_diario.rowconfigure(1, weight=1)

    frame_anotacoes = ttk.Frame(frame_diario, relief="sunken", padding=10)
    frame_anotacoes.grid(row=0, column=9, padx=30, sticky="nwes", rowspan=30)
    frame_anotacoes.rowconfigure(10, weight=1)


def editar_anotacoes(frame_anotacoes, data: datetime, professor):
    global anotacao, nome_antigo
    anotacao = {}
    label_titulo = ttk.Label(
        frame_anotacoes,
        text="Título: ",
        font=(GUI_FONT, 16, "bold"),
    )
    entry_titulo = ttk.Entry(frame_anotacoes)
    anotacao["titulo"] = entry_titulo
    entry_data = ttk.Entry(
        frame_anotacoes, font=(GUI_FONT, 12, "bold"), takefocus=False
    )
    anotacao["data"] = data
    data_formatada = data.strftime("%d/%m/%Y")
    entry_data.insert(0, data_formatada)
    entry_data.config(state="readonly")
    # Descrição
    label_desc = ttk.Label(
        frame_anotacoes, text="Descrição: ", font=(GUI_FONT, 14, "bold")
    )
    entry_desc = tk.Text(
        frame_anotacoes, width=40, height=8, font=(GUI_FONT, 13), padx=5
    )
    scrollbar = tk.Scrollbar(frame_anotacoes, command=entry_desc.yview)
    entry_desc.config(yscrollcommand=scrollbar.set)
    anotacao["desc"] = entry_desc
    # Botões

    def limpar_anotacao(limpar_listbox: bool = False):
        entry_data.config(state="normal")
        entry_data.delete("0", tk.END)
        entry_data.config(state="readonly")
        entry_titulo.delete("0", tk.END)
        entry_desc.delete("1.0", tk.END)
        if limpar_listbox:
            listbox.delete(0, tk.END)

    botao_salvar = ttk.Button(
        frame_anotacoes,
        text="Salvar",
        bootstyle="primary",
        command=lambda: salvar_anotacoes(professor, nome_antigo),
    )
    botao_limpar = ttk.Button(
        frame_anotacoes,
        text="Limpar",
        bootstyle="primary-outline",
        command=lambda: limpar_anotacao(limpar_listbox=True),
    )
    botao_excluir = ttk.Button(
        frame_anotacoes,
        text="Excluir",
        bootstyle="danger-outline",
        command=lambda: excluir_anotacao(professor),
    )
    for i in range(2):
        frame_anotacoes.rowconfigure(i, weight=0)

    def preencher_anotacao(titulo, desc):
        limpar_anotacao()
        entry_titulo.delete("0", tk.END)
        entry_titulo.insert("0", titulo)
        entry_data.config(state="normal")
        entry_data.insert(0, data_formatada)
        entry_data.config(state="readonly")
        entry_desc.delete("1.0", tk.END)
        entry_desc.insert("1.0", desc)

    # Listar Anotações

    print(get_colaborador(professor["cpf"]))
    diario_salvo = get_colaborador(professor["cpf"])["diario"]
    anotacoes_salvas = diario_salvo.get(data.strftime("%d%m%Y"), {})
    listbox = tk.Listbox(frame_anotacoes)

    nome_antigo = None

    items_ordenados = []
    for titulo, desc in anotacoes_salvas.items():
        listbox.insert(tk.END, titulo)
        items_ordenados.append((titulo, desc))

    def editar_nota(event):
        global nome_antigo
        if not listbox.curselection():
            return
        titulo, desc = items_ordenados[listbox.curselection()[0]]
        nome_antigo = titulo
        preencher_anotacao(titulo, desc)

    listbox.bind("<<ListboxSelect>>", editar_nota)

    label_titulo.grid(row=0, column=0, sticky="we")
    entry_titulo.grid(row=0, column=1, sticky="w")
    entry_data.grid(row=0, column=2, sticky="e", padx=10)
    label_desc.grid(row=2, column=0, sticky="nw", pady=10)
    entry_desc.grid(row=3, column=0, columnspan=3, sticky="nwe", padx=(5, 0))
    scrollbar.grid(row=3, column=2, sticky="nes")
    botao_excluir.grid(row=5, column=3, sticky="e", pady=5)
    botao_limpar.grid(row=5, column=4, sticky="e", padx=5, pady=5)
    botao_salvar.grid(row=5, column=5, sticky="w", pady=5)
    listbox.grid(row=6, column=0)


def excluir_anotacao(professor):
    professor = get_colaborador(professor["cpf"])
    data = anotacao["data"].strftime("%d%m%Y")
    titulo = anotacao["titulo"].get()
    diario = professor["diario"].get(data, {})
    if diario.get(titulo, False):
        if messagebox.askyesno(
            "Apagar anotação?", f'Deseja realmente apagar a anotação "{titulo}"?'
        ):
            diario.pop(titulo)
            professor["diario"][data] = diario
            editar_colaborador(professor)
            limpar_widgets(frame_anotacoes)


def salvar_anotacoes(professor, nome_antigo=None):
    data = anotacao["data"].strftime("%d%m%Y")
    titulo = anotacao["titulo"].get()
    desc = anotacao["desc"].get("1.0", "end-1c")

    if not titulo:
        ttk.Label(
            frame_anotacoes,
            text="- Insira um título",
            bootstyle="alert",
            font=(GUI_FONT, 14, "bold"),
        ).grid(row=4, column=0, sticky="w")
        return

    diario_salvo = get_colaborador(professor["cpf"])["diario"]
    anotacoes_salvas = diario_salvo.get(data, {})
    professor = get_colaborador(professor["cpf"])
    diario = professor["diario"].get(data, {})
    if nome_antigo != titulo and titulo in anotacoes_salvas.keys():
        if messagebox.askyesno(
            "Anotação já existente.",
            "Já existe uma nota com este título, deseja substituí-la?",
        ):
            diario.pop(nome_antigo)
        else:
            limpar_widgets(frame_anotacoes)
            return
    diario[titulo] = desc
    professor["diario"][data] = diario
    editar_colaborador(professor)
    limpar_widgets(frame_anotacoes)


if __name__ == "__main__":
    criar_interface_atividades()
