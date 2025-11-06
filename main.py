from dados import checar_json_existe
from seguranca import checar_existencia_env
import ttkbootstrap as ttk
from config import FILES_PATH, GUI_FONT
import tkinter as tk
import locale
import contexto
from telas import (
    tela_login,
    iniciar_cadastro,
    alterar_senha_admin,
    iniciar_edicao_colaborador,
    iniciar_edicao_turma,
    alterar_senha_colaborador,
    iniciar_cadastro_turma,
    iniciar_cadastro_aluno,
    iniciar_edicao_aluno,
    ui_login,
    encerrar,
    alt_tamanho_janela,
    criar_interface_atividades,
    criar_diario,
)


def criar_barra_admin():
    alt_tamanho_janela(1350, 800)

    frame_perfil = tk.Frame(logo_frame)
    frame_perfil.grid(row=0, column=6, sticky="ne")
    nome = " ".join(contexto.colaborador["nome"].split()[0:2])
    ttk.Label(frame_perfil, text=nome, font=(GUI_FONT, 16)).grid(
        row=0, column=0, sticky="n", pady=8
    )

    menubutton_colaboradores = ttk.Menubutton(
        logo_frame, text="Colaboradores", style="Outline.TMenubutton"
    )
    menu_colaboradores = ttk.Menu(
        menubutton_colaboradores,
    )
    menu_colaboradores.add_command(
        label="Novo colaborador",
        command=lambda: iniciar_cadastro(),
    )
    menu_colaboradores.add_command(
        label="Editar colaborador",
        command=lambda: iniciar_edicao_colaborador(),
    )

    menubutton_colaboradores["menu"] = menu_colaboradores
    menubutton_colaboradores.grid(row=0, column=2, pady=3, padx=5, sticky="ne")

    ttk.Separator(
        logo_frame,
        orient=tk.VERTICAL,
        bootstyle="primary",
    ).grid(row=0, column=3, padx=15, sticky="n", pady=2)

    profile = tk.PhotoImage(file=FILES_PATH + "user.png")
    menubutton_profile = ttk.Menubutton(
        frame_perfil, image=profile, style="Outline.TMenubutton"
    )
    menubutton_profile.img = profile
    menu = ttk.Menu(
        menubutton_profile,
    )
    menu.add_command(
        label="Alterar senha",
        command=lambda: alterar_senha_admin(),
    )
    menu.add_command(label="Sair", command=logoff)

    menubutton_profile["menu"] = menu
    menubutton_profile.grid(row=0, column=2, pady=8, padx=5, sticky="n")


def criar_barra_coordenador():
    alt_tamanho_janela(1350, 800)

    # Alunos
    menubutton_alunos = ttk.Menubutton(
        logo_frame, text="Alunos", style="Outline.TMenubutton"
    )
    menu_alunos = ttk.Menu(
        menubutton_alunos,
    )
    menu_alunos.add_command(
        label="Novo Aluno",
        command=lambda: iniciar_cadastro_aluno(),
    )
    menu_alunos.add_command(
        label="Editar Aluno",
        command=lambda: iniciar_edicao_aluno(),
    )

    menubutton_alunos["menu"] = menu_alunos
    menubutton_alunos.grid(row=0, column=1, pady=3, padx=5, sticky="ne")

    ttk.Separator(
        logo_frame,
        orient=tk.VERTICAL,
        bootstyle="primary",
    ).grid(row=0, column=3, padx=15, sticky="n", pady=2)

    # Turmas
    menubutton_turmas = ttk.Menubutton(
        logo_frame, text="Turmas", style="Outline.TMenubutton"
    )
    menu_turmas = ttk.Menu(
        menubutton_turmas,
    )
    menu_turmas.add_command(
        label="Nova Turma",
        command=lambda: iniciar_cadastro_turma(contexto.colaborador),
    )
    menu_turmas.add_command(
        label="Editar Turma",
        command=lambda: iniciar_edicao_turma(),
    )

    menubutton_turmas["menu"] = menu_turmas
    menubutton_turmas.grid(row=0, column=2, pady=3, padx=5, sticky="ne")

    ttk.Separator(
        logo_frame,
        orient=tk.VERTICAL,
        bootstyle="primary",
    ).grid(row=0, column=3, padx=15, sticky="n", pady=2)

    # Profile
    frame_perfil = tk.Frame(logo_frame)
    frame_perfil.grid(row=0, column=6, sticky="ne")
    cargo = "Prof. " if contexto.colaborador["cargo"] == "Professor" else "Coord. "
    nome = cargo + " ".join(contexto.colaborador["nome"].split()[0:2])
    ttk.Label(frame_perfil, text=nome, font=(GUI_FONT, 16)).grid(
        row=0, column=0, sticky="n", pady=8
    )
    profile = tk.PhotoImage(file=FILES_PATH + "user.png")
    menubutton_profile = ttk.Menubutton(
        frame_perfil, image=profile, style="Outline.TMenubutton"
    )
    menubutton_profile.img = profile
    menu = ttk.Menu(
        menubutton_profile,
    )
    menu.add_command(
        label="Alterar senha",
        command=lambda: alterar_senha_colaborador(contexto.colaborador),
    )
    menu.add_command(label="Sair", command=logoff)

    menubutton_profile["menu"] = menu
    menubutton_profile.grid(row=0, column=2, pady=8, padx=5, sticky="n")


# Professor
def criar_barra_professor():
    alt_tamanho_janela(1350, 800)

    # Profile
    frame_perfil = tk.Frame(logo_frame)
    frame_perfil.grid(row=0, column=6, sticky="ne")
    cargo = "Prof. " if contexto.colaborador["cargo"] == "Professor" else "Coord. "
    nome = cargo + " ".join(contexto.colaborador["nome"].split()[0:2])
    ttk.Label(frame_perfil, text=nome, font=(GUI_FONT, 16)).grid(
        row=0, column=0, sticky="n", pady=8
    )
    profile = tk.PhotoImage(file=FILES_PATH + "user.png")
    menubutton_profile = ttk.Menubutton(
        frame_perfil, image=profile, style="Outline.TMenubutton"
    )
    menubutton_profile.img = profile
    menu = ttk.Menu(
        menubutton_profile,
    )
    menu.add_command(
        label="Alterar senha",
        command=lambda: alterar_senha_colaborador(
            contexto.frame_conteudo, contexto.colaborador
        ),
    )
    menu.add_command(label="Sair", command=logoff)

    menubutton_profile["menu"] = menu
    menubutton_profile.grid(row=0, column=2, pady=8, padx=5, sticky="n")

    botao_diario = ttk.Button(
        logo_frame,
        text="Diário",
        command=lambda: criar_diario(contexto.colaborador),
        style="MenuButtons.Primary.TButton",
    )
    botao_atividades = ttk.Button(
        logo_frame,
        text="Atividades",
        command=lambda: criar_interface_atividades(contexto.colaborador),
        style="MenuButtons.Primary.TButton",
    )
    botao_ia = ttk.Button(
        logo_frame,
        text="I.A.",
        command=lambda: print("I.A."),
        style="MenuButtons.Primary.TButton",
    )

    ttk.Separator(
        logo_frame,
        orient=tk.VERTICAL,
        bootstyle="primary",
    ).grid(row=0, column=4, padx=15, sticky="n", pady=2)

    botao_diario.grid(row=0, column=1, pady=5, padx=5, sticky="n")
    botao_atividades.grid(row=0, column=2, pady=5, padx=5, sticky="n")
    botao_ia.grid(row=0, column=3, pady=5, padx=5, sticky="n")


def logoff():
    contexto.colaborador = {}

    for widget in contexto.janela.winfo_children():
        widget.destroy()

    login()


def login():
    global logo_frame
    ui_login()

    contexto.colaborador = tela_login()
    contexto.colaborador["nome"] = contexto.colaborador.get("nome", "Administrador")

    contexto.frame_conteudo = tk.Frame(contexto.janela)
    contexto.frame_conteudo.grid(row=2, column=0, sticky="nsew", padx=10)
    contexto.frame_conteudo.grid_propagate(True)
    if contexto.colaborador:
        contexto.janela.login_logo_frame.destroy()
        # UI
        contexto.janela.columnconfigure(0, weight=1)
        logo_frame = tk.Frame(
            contexto.janela,
            padx=10,
            relief="solid",
        )
        logo_frame.columnconfigure(0, weight=1)
        logo_frame.grid(row=0, column=0, sticky="ew")
        logo = tk.PhotoImage(file=FILES_PATH + "EduSmart2.png")
        label_logo = tk.Label(logo_frame, image=logo)
        label_logo.img = logo
        label_logo.grid(row=0, column=0, sticky="nw")

        ttk.Separator(logo_frame, orient=tk.HORIZONTAL).grid(
            row=1, column=0, columnspan=10, sticky="nwe"
        )
        # Checa por cargo
        if contexto.colaborador.get("login", None) == "Admin":
            criar_barra_admin()
        elif contexto.colaborador.get("cargo", None) == "Coordenador":
            criar_barra_coordenador()
        elif contexto.colaborador.get("cargo", None) == "Professor":
            criar_barra_professor()


def main():
    checar_existencia_env()
    checar_json_existe()

    contexto.janela = ttk.Window()
    # Estilo
    style = ttk.Style(theme="cosmo")
    style.configure("TButton", font=(GUI_FONT, 13))
    style.configure(
        "Outline.TMenubutton",
        bordercolor="white",
        font=(GUI_FONT, 16),
        foreground="black",
        arrowcolor="black",
    )
    # Botões barra menu
    style.configure(
        "MenuButtons.Primary.TButton",
        font=(GUI_FONT, 16),
        borderwidth=0,
        background="white",
        foreground="black",
    )
    style.map(
        "MenuButtons.Primary.TButton",
        background=[("active", "#EEF3FD")],
        foreground=[("active", "black")],
    )

    contexto.janela.option_add("*Menu.font", (GUI_FONT, 15))

    contexto.janela.protocol("WM_DELETE_WINDOW", encerrar)
    contexto.janela.title("EduSmart")
    contexto.janela.iconbitmap(FILES_PATH + "EduSmart.ico")
    alt_tamanho_janela(500, 500)
    contexto.janela.rowconfigure(0, weight=0, minsize=10)
    contexto.janela.rowconfigure(1, weight=0)
    contexto.janela.rowconfigure(2, weight=1)

    contexto.frame_conteudo = tk.Frame(contexto.janela)

    login()

    contexto.janela.mainloop()


locale.setlocale(locale.LC_TIME, "pt_BR")

if __name__ == "__main__":
    main()
