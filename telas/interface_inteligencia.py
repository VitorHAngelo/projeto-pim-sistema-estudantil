import contexto
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from config import GUI_FONT
import threading
from gemini_api import enviar_mensagem_gemini
from dados import get_turma, get_aluno_by_ra

arvore = {
    "Escolher categoria": {
        "Aluno": {
            "Informações disponíveis": {"Notas": "Exibir notas do aluno selecionado"}
        },
        "Turmas": {
            "Informações disponíveis": {
                "Atividades": "Exibir atividades da turma",
                "Frequência": "Exibir frequência da turma",
                "Alunos": "Listar alunos da turma",
            }
        },
    }
}


def criar_frame_chat():
    for widget in contexto.frame_conteudo.winfo_children():
        widget.destroy()

    frame_chat = ttk.Frame(contexto.frame_conteudo)
    frame_chat.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    frame_chat.rowconfigure(0, weight=1)
    frame_chat.columnconfigure(0, weight=1)

    frame_chat_container = ttk.Frame(frame_chat)
    frame_chat_container.pack(expand=True)

    frame_linha = ttk.Frame(frame_chat_container)
    frame_linha.grid(row=0, column=0, sticky="nsew")

    frame_chat_container.rowconfigure(0, weight=1)
    frame_chat_container.columnconfigure(0, weight=1)

    frame_canvas = ttk.Frame(frame_linha)
    frame_canvas.grid(row=0, column=0, sticky="nsew")

    canvas = tk.Canvas(
        frame_canvas, width=800, height=500, highlightthickness=0, bg="white"
    )
    canvas.grid(row=0, column=0, pady=10, padx=(0, 10))

    scrollbar = ttk.Scrollbar(frame_canvas, orient=VERTICAL, command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns", pady=10)
    canvas.configure(yscrollcommand=scrollbar.set)

    frame_anexo = ttk.Frame(frame_linha, width=250, padding=10)
    frame_anexo.grid(row=0, column=1, sticky="n", padx=(0, 10), pady=(10, 0))

    frame_linha.columnconfigure(0, weight=1)
    frame_linha.columnconfigure(1, weight=0)

    frame_mensagens = ttk.Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=frame_mensagens, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_mensagens.bind("<Configure>", on_frame_configure)

    def _on_mousewheel(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def _bound(event):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _unbound(event):
        canvas.unbind_all("<MouseWheel>")

    frame_canvas.bind("<Enter>", _bound)
    frame_canvas.bind("<Leave>", _unbound)

    frame_input = ttk.Frame(frame_linha)
    frame_input.grid(row=1, column=0, sticky="w", pady=(5, 10))

    txt_mensagem = ttk.Text(frame_input, height=3, wrap="word", font=(GUI_FONT, 14))
    txt_mensagem.pack(side="left", padx=(0, 10))
    btn_enviar = ttk.Button(frame_input, text="Enviar", bootstyle="primary")
    btn_enviar.pack(side="left")
    frame_linha.rowconfigure(1, weight=0)

    criar_frame_anexo(frame_anexo)

    def adicionar_mensagem(texto, remetente="usuário"):
        msg_frame = ttk.Frame(frame_mensagens)
        msg_frame.pack(
            fill="x", pady=4, padx=10, anchor="e" if remetente == "usuário" else "w"
        )

        estilo = "primary" if remetente == "usuário" else "secondary"
        rotulo = ttk.Label(
            msg_frame,
            text=texto,
            wraplength=600,
            bootstyle=estilo,
            justify=RIGHT if remetente == "usuário" else LEFT,
            padding=8,
            font=(GUI_FONT, 15),
        )
        rotulo.pack(anchor="e" if remetente == "usuário" else "w")

        canvas.update_idletasks()
        canvas.yview_moveto(1.0)

    def enviar_mensagem(event=None):
        texto = txt_mensagem.get("1.0", tk.END).strip()
        if not texto:
            return

        adicionar_mensagem(texto, "usuário")
        txt_mensagem.delete("1.0", tk.END)
        adicionar_mensagem("Pensando...", "ia")

        thread = threading.Thread(target=processar_resposta_ia, args=(texto,))
        thread.daemon = True
        thread.start()

    def processar_resposta_ia(texto_usuario):
        resposta = enviar_mensagem_gemini(texto_usuario, anexo)
        contexto.frame_conteudo.after(0, lambda: adicionar_mensagem(resposta, "ia"))

    def ignorar_shift_enter(event):
        return

    btn_enviar.config(command=enviar_mensagem)
    txt_mensagem.bind("<Shift-Return>", ignorar_shift_enter)
    txt_mensagem.bind("<Return>", enviar_mensagem)

    return frame_chat


def criar_frame_anexo(frame):
    global anexo
    for w in frame.winfo_children():
        w.destroy()

    if "anexo" not in globals():
        anexo = None

    frame_anexo = ttk.Frame(frame, padding=10)
    frame_anexo.pack(fill=X, padx=10, pady=10)

    label_titulo = ttk.Label(
        frame_anexo, text="Deseja adicionar algum dado?", font=(GUI_FONT, 16, "bold")
    )
    label_titulo.pack(side="top")

    topo = ttk.Frame(frame_anexo)
    topo.pack(fill=X)

    tipo_anexo = tk.StringVar(value="Escolher tipo")

    menu = ttk.Menubutton(topo, textvariable=tipo_anexo, bootstyle="primary-outline")
    menu.pack(side=LEFT, padx=(0, 10))

    menu.menu = tk.Menu(menu, tearoff=0)
    menu["menu"] = menu.menu

    def escolher_tipo(valor):
        tipo_anexo.set(valor)
        atualizar_opcoes(valor)

    menu.menu.add_command(label="Aluno", command=lambda: escolher_tipo("Aluno"))
    menu.menu.add_command(label="Turma", command=lambda: escolher_tipo("Turma"))

    frame_opcoes = ttk.Frame(frame_anexo)
    frame_opcoes.pack(fill=X, pady=(10, 0))

    btn_buscar_ref = {"btn": None}

    def limpar():
        global anexo
        anexo = None
        tipo_anexo.set("Escolher tipo")
        for w in frame_opcoes.winfo_children():
            w.destroy()
        if btn_buscar_ref["btn"]:
            btn_buscar_ref["btn"].config(bootstyle="secondary-outline")

    btn_cancelar = ttk.Button(
        topo, text="❌", width=3, bootstyle="danger-outline", command=limpar
    )
    btn_cancelar.pack(side="left")

    def redefinir_btn_busca(btn):
        btn.config(bootstyle="primary")

    def atualizar_opcoes(tipo):
        for w in frame_opcoes.winfo_children():
            w.destroy()

        if tipo == "Turma":
            lbl = ttk.Label(
                frame_opcoes,
                text="Escolha o dado da turma:",
                font=(GUI_FONT, 11, "bold"),
            )
            lbl.pack(anchor="w", pady=(0, 5))

            opcao_turma = tk.StringVar(value="Atividades")
            for opcao in ["Atividades", "Frequencia", "Alunos"]:
                ttk.Radiobutton(
                    frame_opcoes,
                    text=opcao,
                    variable=opcao_turma,
                    value=opcao,
                    bootstyle="info",
                ).pack(anchor="w")

            ttk.Label(frame_opcoes, text="Sigla da turma:").pack(
                anchor="w", pady=(10, 0)
            )
            frame_entry = ttk.Frame(frame_opcoes)
            frame_entry.pack(anchor="w", pady=2, fill=X)

            entry_turma = ttk.Entry(frame_entry, width=25)
            entry_turma.bind(
                "<KeyPress>",
                lambda event: (
                    redefinir_btn_busca(btn_buscar_ref["btn"])
                    if btn_buscar_ref["btn"]
                    else None
                ),
            )
            entry_turma.pack(side=LEFT, fill=X, expand=True)

            btn_buscar = ttk.Button(
                frame_entry,
                text="🔍",
                width=3,
                bootstyle="secondary-outline",
                command=lambda: buscar(tipo, entry_turma, opcao_turma),
            )
            btn_buscar.pack(side=LEFT, padx=(5, 0))
            btn_buscar_ref["btn"] = btn_buscar

        elif tipo == "Aluno":
            ttk.Label(frame_opcoes, text="Digite o RA do aluno:").pack(
                anchor="w", pady=(5, 0)
            )
            frame_entry = ttk.Frame(frame_opcoes)
            frame_entry.pack(anchor="w", pady=2, fill=X)

            entry_aluno = ttk.Entry(frame_entry, width=25)
            entry_aluno.bind(
                "<KeyPress>",
                lambda event: (
                    redefinir_btn_busca(btn_buscar_ref["btn"])
                    if btn_buscar_ref["btn"]
                    else None
                ),
            )
            entry_aluno.pack(side=LEFT, fill=X, expand=True)

            btn_buscar = ttk.Button(
                frame_entry,
                text="🔍",
                width=3,
                bootstyle="secondary-outline",
                command=lambda: buscar(tipo, entry_aluno),
            )
            btn_buscar.pack(side=LEFT, padx=(5, 0))
            btn_buscar_ref["btn"] = btn_buscar

    def buscar(
        tipo: str,
        parametro: ttk.Entry,
        escolha: str = None,
    ):
        global anexo
        if tipo == "Turma":
            dados_turma = get_turma(parametro.get().upper())
            if not dados_turma:
                btn_buscar_ref["btn"].config(bootstyle="danger", text="❌")
                return None

            btn_buscar_ref["btn"].config(bootstyle="success", text="✔️")
            anexo = dados_turma[escolha.get().lower()]

        elif tipo == "Aluno":
            dados_aluno = get_aluno_by_ra(parametro.get().upper())
            if not dados_aluno:
                btn_buscar_ref["btn"].config(bootstyle="danger", text="❌")
                return None
            lista_dados = {"nome": dados_aluno["nome"], "notas": dados_aluno["notas"]}
            anexo = lista_dados
            btn_buscar_ref["btn"].config(bootstyle="success", text="✔️")

    return frame_anexo
