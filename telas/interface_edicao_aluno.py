import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from dados import add_aluno, get_aluno_by_cpf, get_aluno_by_ra, get_alunos_by_name
from telas.utils_tk import limpar_widgets


FONTE = "Calibri"
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


def cadastrar():
    dados_aluno = {}
    erros = []
    # CPF
    cpf = "".join([digit for digit in aluno["cpf"].get() if digit.isdigit()])
    if len(cpf) != 11:
        frame_edicao_aluno.label_cpf_invalido.config(text="CPF Inválido.")
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
    if not "@" in aluno["email"].get() or not "." in aluno["email"].get():
        erros.append("- Email inválido.")
    frame_erros = tk.Frame(frame_edicao_aluno, width=100, height=100)
    for i in range(6):
        frame_erros.rowconfigure(i, minsize=5, weight=1)
    frame_erros.grid(row=7, column=0)
    if erros:
        for i in range(len(erros)):
            tk.Label(
                frame_erros, text=erros[i], fg="red", font=(FONTE, 14, "bold")
            ).grid(row=i, column=0, sticky="w")
        return
    dados_aluno[cpf] = {
        "nome": aluno["nome"].get(),
        "nascimento": nascimento,
        "email": aluno["email"].get(),
        "telefone": telefone,
        "telefone_resp": telefone_resp,
        "obs": aluno["obs"].get("1.0", "end-1c"),
    }
    status = add_aluno(dados_aluno)
    if status[0] in (1, 2):  # Se código for 1 ou 2
        limpar_widgets(frame_edicao_aluno)
    messagebox.showinfo(
        "Cadastro", message=status[1], icon="info", parent=frame_edicao_aluno
    )


def limpar():
    for widget in frame_edicao_aluno.winfo_children():
        widget.destroy()


def mudar_selecao(event, entry: tk.Entry):
    entry.delete(0, tk.END)
    entry.focus()


def atalho_enter(event):
    if event.state in (40, 42, 262184, 262186) and event.keysym == "Return":
        cadastrar()


def formatar_telefone(event, campo, entry):
    if event.state in (40, 262184) and event.keysym in TECLAS_IGNORADAS:
        return
    telefone = [char for char in campo.get() if char.isdigit()]
    if len(telefone) == 10:
        telefone.insert(0, "(")
        telefone.insert(3, ")")
        telefone.insert(8, "-")
        entry.delete(0, tk.END)
        entry.insert(0, "".join(telefone))
    else:
        telefone.insert(0, "(")
        telefone.insert(3, ")")
        telefone.insert(9, "-")
        entry.delete(0, tk.END)
        entry.insert(0, "".join(telefone[0:14]))


def formatar_cpf(event, campo, entry, tipo_busca):
    if event.state in (40, 262184) and event.keysym in TECLAS_IGNORADAS:
        return
    if tipo_busca.get() != "CPF":
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


def verificar_email(event, campo, entry):
    email = list(campo.get())
    if not "@" in email or not "." in email or " " in email:
        entry.config(fg="red")
    else:
        entry.config(fg="black")


def verificar_data(event, campo, entry):
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


def reconstruir_frame(frame_conteudo):
    limpar_widgets(frame_conteudo)

    global frame_edicao_aluno
    global aluno

    frame_edicao_aluno = tk.Frame(frame_conteudo)

    for i in range(1, 10):
        frame_edicao_aluno.rowconfigure(i, minsize=20)
    # frame_cadastro.rowconfigure(8, minsize=250, weight=1)
    frame_edicao_aluno.columnconfigure((0, 6), minsize=10)
    frame_edicao_aluno.columnconfigure((1, 2, 3, 4, 5), pad=5, weight=0, minsize=10)
    frame_edicao_aluno.grid(row=0, column=0, sticky="sew", pady=15)

    # Nome
    label_nome = tk.Label(frame_edicao_aluno, text="Nome: ", font=(FONTE, 16, "bold"))
    campo_nome = tk.StringVar()
    entry_nome = tk.Entry(frame_edicao_aluno, textvariable=campo_nome, font=(FONTE, 16))
    aluno["nome"] = campo_nome
    entry_nome.bind("<KeyPress>", atalho_enter)
    entry_nome.focus()

    # Data Nascimento
    label_nascimento = tk.Label(
        frame_edicao_aluno, text="Nascimento: ", font=(FONTE, 16, "bold")
    )
    campo_nascimento = tk.StringVar()
    entry_nascimento = tk.Entry(
        frame_edicao_aluno, textvariable=campo_nascimento, font=(FONTE, 16)
    )
    aluno["nascimento"] = campo_nascimento
    entry_nascimento.bind("<Return>", atalho_enter)
    entry_nascimento.bind(
        "<KeyPress>",
        lambda event: verificar_data(event, campo_nascimento, entry_nascimento),
    )

    # CPF
    label_cpf = tk.Label(frame_edicao_aluno, text="CPF: ", font=(FONTE, 16, "bold"))
    frame_edicao_aluno.label_cpf_invalido = tk.Label(
        frame_edicao_aluno,
        text="",
        font=(FONTE, 16, "bold"),
        fg="red",
    )
    campo_cpf = tk.StringVar()
    entry_cpf = tk.Entry(frame_edicao_aluno, textvariable=campo_cpf, font=(FONTE, 16))
    aluno["cpf"] = campo_cpf
    entry_cpf.bind("<Return>", atalho_enter)
    entry_cpf.bind(
        "<KeyPress>", lambda event: formatar_cpf(event, campo_cpf, entry_cpf)
    )

    # Email
    label_email = tk.Label(
        frame_edicao_aluno, text="E-mail: ", font=(FONTE, 16, "bold")
    )
    campo_email = tk.StringVar()
    entry_email = tk.Entry(
        frame_edicao_aluno, textvariable=campo_email, font=(FONTE, 16)
    )
    aluno["email"] = campo_email
    entry_email.bind("<Return>", atalho_enter)
    entry_email.bind(
        "<KeyPress>", lambda event: verificar_email(event, campo_email, entry_email)
    )
    label_validacao_email = tk.Label(
        frame_edicao_aluno, text="Digite um email válido.", font=(FONTE, 12, "bold")
    )

    # Telefone
    label_telefone = tk.Label(
        frame_edicao_aluno, text="Telefone: ", font=(FONTE, 16, "bold")
    )
    campo_telefone = tk.StringVar()
    entry_telefone = tk.Entry(
        frame_edicao_aluno, textvariable=campo_telefone, font=(FONTE, 16)
    )
    aluno["telefone"] = campo_telefone
    entry_telefone.bind("<Return>", atalho_enter)
    entry_telefone.bind(
        "<KeyPress>",
        lambda event: formatar_telefone(event, campo_telefone, entry_telefone),
    )

    # Telefone2
    label_telefone_resp = tk.Label(
        frame_edicao_aluno, text="Telefone/Responsável: ", font=(FONTE, 16, "bold")
    )
    campo_telefone_resp = tk.StringVar()
    entry_telefone_resp = tk.Entry(
        frame_edicao_aluno, textvariable=campo_telefone_resp, font=(FONTE, 16)
    )
    aluno["telefone_resp"] = campo_telefone_resp
    entry_telefone_resp.bind("<Return>", atalho_enter)
    entry_telefone_resp.bind(
        "<KeyPress>",
        lambda event: formatar_telefone(
            event, campo_telefone_resp, entry_telefone_resp
        ),
    )

    # Observacoes
    label_obs = tk.Label(
        frame_edicao_aluno, text="Observações: ", font=(FONTE, 16, "bold")
    )
    entry_obs = tk.Text(frame_edicao_aluno, width=60, height=6, font=(FONTE, 12))
    scrollbar = tk.Scrollbar(frame_edicao_aluno, command=entry_obs.yview)
    aluno["obs"] = entry_obs
    entry_obs.config(yscrollcommand=scrollbar.set)

    # Popular campos
    entry_nome.insert(0, usuario_buscado["nome"])
    entry_cpf.insert(0, usuario_buscado["cpf"])
    entry_email.insert(0, usuario_buscado["email"])
    entry_nascimento.insert(0, usuario_buscado["nascimento"])
    entry_telefone.insert(0, usuario_buscado["telefone"])
    entry_cpf.config(state="readonly")
    campo_cargo.set(usuario_buscado["cargo"])

    # Botões
    botao_salvar = tk.Button(
        frame_edicao_aluno, text="Salvar", font=(FONTE, 14, "bold"), command=cadastrar
    )
    botao_limpar = tk.Button(
        frame_edicao_aluno, text="Limpar", font=(FONTE, 14), command=limpar
    )
    botao_cancelar = tk.Button(
        frame_edicao_aluno, text="Cancelar", font=(FONTE, 14), command=cancelar
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
    entry_obs.grid(row=5, column=0, ipady=10, columnspan=3, sticky="w", padx=15)
    scrollbar.grid(row=5, column=2, sticky="nse")

    # Row 8
    botao_cancelar.grid(row=8, column=4, sticky="es", ipady=10, padx=2)
    botao_limpar.grid(row=8, column=5, sticky="wes", ipady=10, padx=2)
    botao_salvar.grid(row=8, column=6, sticky="wes", ipady=10, padx=2)


def editar_com_ra(ra):
    return reconstruir_frame(get_aluno_by_ra(ra))


def interface_busca(frame_conteudo):
    global frame_busca_aluno
    frame_busca_aluno = tk.Frame(frame_conteudo)
    limpar_widgets(frame_busca_aluno)
    label_busca = tk.Label(
        frame_busca_aluno,
        text="Busque pelo aluno:",
        font=(FONTE, 16, "bold"),
        padx=20,
    )
    campo_busca = tk.StringVar()
    entry_busca = tk.Entry(
        frame_busca_aluno, textvariable=campo_busca, font=(FONTE, 16)
    )
    entry_busca.bind(
        "<Return>",
        lambda event: buscar_colaborador(
            frame_conteudo, entry_busca, campo_busca.get(), tipo_busca.get(), event
        ),
    )
    entry_busca.bind(
        "<KeyPress>",
        lambda event: formatar_cpf(event, campo_busca, entry_busca, tipo_busca),
    )
    tipo_busca = ttk.Combobox(
        frame_busca_aluno, values=["RA", "CPF", "Nome"], font=(FONTE, 12), width=8
    )
    tipo_busca.bind(
        "<<ComboboxSelected>>", lambda event: mudar_selecao(event, entry_busca)
    )
    tipo_busca.set("RA")

    botao_buscar = tk.Button(
        frame_busca_aluno,
        text="Buscar",
        command=lambda: buscar_colaborador(
            frame_conteudo, entry_busca, campo_busca.get(), tipo_busca.get()
        ),
    )

    frame_busca_aluno.grid()
    frame_busca_aluno.columnconfigure((1, 2, 3, 4, 5), minsize=5)
    label_busca.grid(row=0, column=0, pady=10, sticky="e")
    entry_busca.grid(row=0, column=1, sticky="we")
    tipo_busca.grid(row=0, column=3, sticky="w", padx=5)
    botao_buscar.grid(row=0, column=4, sticky="w")


def buscar_colaborador(
    frame_conteudo, entry_busca, campo_busca: str, tipo_busca, event=None
):
    aluno = None
    match tipo_busca:
        case "RA":
            aluno = get_aluno_by_ra(campo_busca.upper())
            reconstruir_frame(aluno)
        case "CPF":
            cpf = "".join([digit for digit in campo_busca if digit.isdigit()])
            aluno = get_aluno_by_cpf(cpf)
            reconstruir_frame(aluno)
        case "Nome":
            nomes = get_alunos_by_name(campo_busca)
            print(nomes)
            global canvas_nomes_alunos
            canvas_nomes_alunos = tk.Canvas(frame_busca_aluno, width=500, height=500)
            canvas_nomes_alunos.grid(
                row=4, column=0, rowspan=8, columnspan=3, pady=10, padx=(30, 0)
            )
            canvas_nomes_alunos.columnconfigure(1, minsize=60)
            tk.Label(frame_busca_aluno, text="Nome", font=(FONTE, 16, "bold")).grid(
                row=1, column=0, sticky="we", padx=(33, 0)
            )
            tk.Label(frame_busca_aluno, text="RA", font=(FONTE, 16, "bold")).grid(
                row=1, column=1, sticky="w", padx=(58, 0)
            )

            frame_nomes_alunos = tk.Frame(canvas_nomes_alunos)
            canvas_nomes_alunos.create_window(
                (0, 4),
                window=frame_nomes_alunos,
                anchor="nw",
            )
            frame_nomes_alunos.columnconfigure(1, minsize=200)

            scrollbar = ttk.Scrollbar(
                frame_busca_aluno, orient="vertical", command=canvas_nomes_alunos.yview
            )
            canvas_nomes_alunos.configure(yscrollcommand=scrollbar.set)

            def atualizar_scroll(event):
                canvas_nomes_alunos.configure(
                    scrollregion=canvas_nomes_alunos.bbox("all")
                )

            frame_nomes_alunos.bind("<Configure>", atualizar_scroll)
            i = 2
            for nome, ra in nomes.items():
                tk.Button(
                    frame_nomes_alunos,
                    command=lambda ra=ra: editar_com_ra(ra),
                    text=nome,
                    border=0,
                    font=(FONTE, 14),
                ).grid(row=i, column=1, sticky="we")
                tk.Button(
                    frame_nomes_alunos,
                    command=lambda ra=ra: editar_com_ra(ra),
                    text=ra,
                    border=0,
                    font=(FONTE, 14),
                ).grid(row=i, column=2, padx=(40, 0))
                i += 1
            scrollbar.grid(
                row=1,
                column=0,
                rowspan=20,
                sticky="nsw",
            )
            aluno = get_aluno_by_ra()
    return
    if aluno != None:
        reconstruir_frame(frame_conteudo, aluno)
    else:
        messagebox.showinfo("Inválido.", message="Aluno não localizado.")
        iniciar_edicao_aluno(frame_conteudo)


def iniciar_edicao_aluno(frame_conteudo):
    limpar_widgets(frame_conteudo)
    usuario_buscado = interface_busca(frame_conteudo)


aluno = {}


if __name__ == "__main__":
    iniciar_edicao_aluno()
