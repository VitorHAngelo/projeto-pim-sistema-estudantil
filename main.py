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
    criar_interface_frequencia,
    criar_frame_chat,
)


def criar_barra_admin():
    """Cria a barra de ferramentas para o usuário Admin.

    Ajusta o tamanho da janela, monta o menu de colaboradores, o menu de perfil
    (com opções para alterar a senha e sair) e exibe o nome do colaborador
    atual. Também adiciona o botão/ícone de perfil e o separador visual.

    Efeitos colaterais:
    - Modifica a interface global (`logo_frame`, widgets dentro dele).
    - Utiliza e atualiza `contexto.colaborador`.
    - Chama `mensagem_eco` para adicionar o botão de sustentabilidade.
    """
    alt_tamanho_janela(1350, 800)

    frame_perfil = tk.Frame(logo_frame)
    frame_perfil.grid(row=0, column=6, sticky="ne")
    nome = " ".join(contexto.colaborador["nome"].split()[0:2])
    ttk.Label(frame_perfil, text=nome, font=(GUI_FONT, 16)).grid(
        row=0, column=0, sticky="n", pady=8
    )

    mensagem_eco(frame_perfil)

    menubutton_colaboradores = ttk.Menubutton(
        logo_frame, text="Colaboradores", style="Outline.TMenubutton"
    )
    menu_colaboradores = ttk.Menu(
        menubutton_colaboradores,
    )
    menu_colaboradores.add_command(
        label="Novo colaborador",
        command=iniciar_cadastro,
    )
    menu_colaboradores.add_command(
        label="Editar colaborador",
        command=iniciar_edicao_colaborador,
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
        command=alterar_senha_admin,
    )
    menu.add_command(label="Sair", command=logoff)

    menubutton_profile["menu"] = menu
    menubutton_profile.grid(row=0, column=2, pady=8, padx=5, sticky="n")


def criar_barra_coordenador():
    """Cria a barra de ferramentas para o usuário Coordenador.

    Define botões e menus relevantes para coordenadores (Alunos, Turmas e I.A.),
    além de exibir o perfil do colaborador atual. Ajusta também o tamanho da
    janela para a resolução adequada.

    Efeitos colaterais:
    - Modifica a interface global (`logo_frame`).
    - Usa `contexto.colaborador` para montar o texto do perfil.
    """
    alt_tamanho_janela(1350, 800)

    # Alunos
    menubutton_alunos = ttk.Menubutton(
        logo_frame, text="Alunos", style="MenuButtons.Primary.TButton"
    )
    menu_alunos = ttk.Menu(
        menubutton_alunos,
    )
    menu_alunos.add_command(
        label="Novo Aluno",
        command=iniciar_cadastro_aluno,
    )
    menu_alunos.add_command(
        label="Editar Aluno",
        command=iniciar_edicao_aluno,
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
        logo_frame, text="Turmas", style="MenuButtons.Primary.TButton"
    )
    menu_turmas = ttk.Menu(
        menubutton_turmas,
    )
    menu_turmas.add_command(
        label="Nova Turma",
        command=iniciar_cadastro_turma,
    )
    menu_turmas.add_command(
        label="Editar Turma",
        command=iniciar_edicao_turma,
    )

    menubutton_turmas["menu"] = menu_turmas
    menubutton_turmas.grid(row=0, column=2, pady=3, padx=5, sticky="ne")

    # IA

    botao_ia = ttk.Button(
        logo_frame,
        text="I.A.",
        command=criar_frame_chat,
        style="MenuButtons.Primary.TButton",
    )
    botao_ia.grid(row=0, column=3, pady=3, padx=5, sticky="ne")

    ttk.Separator(
        logo_frame,
        orient=tk.VERTICAL,
        bootstyle="primary",
    ).grid(row=0, column=4, padx=15, sticky="n", pady=2)

    # Profile
    frame_perfil = tk.Frame(logo_frame)
    frame_perfil.grid(row=0, column=6, sticky="ne")
    mensagem_eco(frame_perfil)
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
    """Cria a barra de ferramentas para o usuário Professor.

    Monta o perfil, botões de acesso rápido (Diário, Frequência, Atividades, I.A.)
    e o menu de perfil com opção para alterar senha e sair. Ajusta o tamanho da
    janela quando necessário.

    Efeitos colaterais:
    - Modifica `logo_frame` e adiciona widgets ao topo da janela.
    - Usa `contexto.colaborador` para decidir o rótulo do usuário.
    """
    alt_tamanho_janela(1350, 800)

    # Profile
    frame_perfil = tk.Frame(logo_frame)
    mensagem_eco(frame_perfil)
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
        command=criar_diario,
        style="MenuButtons.Primary.TButton",
    )
    botao_frequencia = ttk.Button(
        logo_frame,
        text="Frequência",
        command=criar_interface_frequencia,
        style="MenuButtons.Primary.TButton",
    )
    botao_atividades = ttk.Button(
        logo_frame,
        text="Atividades",
        command=criar_interface_atividades,
        style="MenuButtons.Primary.TButton",
    )
    botao_ia = ttk.Button(
        logo_frame,
        text="I.A.",
        command=criar_frame_chat,
        style="MenuButtons.Primary.TButton",
    )

    botao_diario.grid(row=0, column=1, pady=5, padx=5, sticky="n")
    botao_frequencia.grid(row=0, column=2, pady=5, padx=5, sticky="n")
    botao_atividades.grid(row=0, column=3, pady=5, padx=5, sticky="n")
    botao_ia.grid(row=0, column=4, pady=5, padx=5, sticky="n")

    ttk.Separator(
        logo_frame,
        orient=tk.VERTICAL,
        bootstyle="primary",
    ).grid(row=0, column=5, padx=15, sticky="n", pady=2)


def mostrar_mensagem_eco(num_mensagem=1):
    """Exibe um popup com mensagem(s) sobre sustentabilidade.

    Parâmetros:
    - num_mensagem (int): se 1 exibe a primeira mensagem, caso contrário a segunda.

    O popup é centralizado na tela e contém botões para navegar entre as
    mensagens e fechar a janela.
    """
    popup = ttk.Toplevel()
    popup.title("Sustentabilidade")
    popup.geometry("880x480")
    popup.update_idletasks()
    largura = popup.winfo_width()
    altura = popup.winfo_height()
    x = popup.winfo_screenwidth() // 2 - largura // 2
    y = popup.winfo_screenheight() // 2 - altura // 2
    popup.geometry(f"+{x}+{y}")

    frame_mensagem = ttk.Frame(master=popup)
    frame_mensagem.grid(row=0, column=0)
    popup.rowconfigure(0, weight=1)
    popup.columnconfigure(1, weight=1)

    def mudar_mensagem(num):
        """Fecha o popup atual e reabre mostrando a mensagem indicada.

        Este helper é usado pelos botões de navegação dentro do popup.
        """
        popup.destroy()
        mostrar_mensagem_eco(num)

    def mensagem_um():
        """Popula o popup com a primeira mensagem sobre educação ambiental.

        Essa função cria os widgets (label e botão) para a primeira tela de
        conteúdo do popup.
        """
        mensagem = """    A educação ambiental é o processo de aprendizagem que visa entender
e respeitar o meio ambiente, tendo uma conscientização sobre nossas atitudes e seu
impacto sobre o planeta. Ela vai além das aulas de ciência ou de campanhas de reciclagem,
ela também coopera para desenvolver uma mentalidade sustentável capaz de equilibrar o
avanço tecnológico e o cuidado com o meio ambiente. 
    A educação ambiental  é de extrema importância tendo em vista que ela pode
transformar comportamentos e gerar mudanças reais na sociedade. Em nosso planeta,
onde é marcado pelo alto índice de produção de lixo, degradação ambiental entre
outros danos, é necessário repensar formas de minimizar esses altos índices.
Dentro de nossa escola ou até mesmo fora, essa conscientização ganha mais relevância
ainda pois os conhecimentos podem ser aplicados de maneira prática em nosso
cotidiano, formando assim alunos com práticas sustentáveis. 
"""
        ttk.Label(
            frame_mensagem,
            text=mensagem,
            font=(GUI_FONT, 14),
            bootstyle="primary",
            justify="center",
        ).grid(row=1, column=1, columnspan=5)
        ttk.Button(
            frame_mensagem,
            text=">",
            bootstyle="primary-outline",
            command=lambda: mudar_mensagem(2),
        ).grid(row=2, column=5, sticky="e")

    def mensagem_dois():
        """Popula o popup com a segunda mensagem sobre sustentabilidade.

        Essa função cria os widgets (label e botão) para a segunda tela de
        conteúdo do popup.
        """
        mensagem = """    A sustentabilidade não é somente uma teoria, mas um estilo
de vida e boas práticas que se constroem por meio de atitudes diárias. Alguns hábitos
que podemos colocar em prática em nosso cotidiano: 
- Separar o lixo corretamente
- Economizar água e energia elétrica
- Reduzir o uso de plásticos e optar por materiais reutilizáveis
- Utilizar transportes coletivos 
- Participar de campanhas e projetos ambientais
Esses hábitos por menores que parecem ser, podem impactar grandemente e positivamente
no meio ambiente se forem colocados em prática de forma coletiva. A educação ambiental
mostra que cada pessoa pode e deve contribuir para um planeta mais saudável e preservado.
    Sendo assim, cuidar do meio ambiente é cuidar das próximas gerações!

"O meio ambiente é o livro aberto da natureza, e cada um de nós escreve uma página.\""""
        ttk.Label(
            frame_mensagem,
            text=mensagem,
            font=(GUI_FONT, 14),
            bootstyle="primary",
            justify="left",
        ).grid(row=1, column=1, columnspan=5)
        ttk.Button(
            frame_mensagem,
            text="<",
            bootstyle="primary-outline",
            command=lambda: mudar_mensagem(1),
        ).grid(row=2, column=1, sticky="w")

    titulo = "Educação Ambiental: consciência, responsabilidade e ação.\n"
    ttk.Label(
        frame_mensagem,
        text=titulo,
        font=(GUI_FONT, 18, "bold"),
        bootstyle="primary",
        justify="center",
    ).grid(row=0, column=1, columnspan=5)
    big_leaf = tk.PhotoImage(master=frame_mensagem, file=FILES_PATH + "leaf_big.png")
    imagem_leaf = ttk.Label(frame_mensagem, image=big_leaf, padding=40)
    imagem_leaf.img = big_leaf
    imagem_leaf.grid(row=0, column=0, sticky="ns", rowspan=3)
    ttk.Button(
        frame_mensagem,
        text="Fechar",
        bootstyle="primary-outline",
        command=popup.destroy,
    ).grid(row=3, column=3)
    if num_mensagem == 1:
        mensagem_um()
    else:
        mensagem_dois()


def mensagem_eco(frame_perfil):
    """Insere um botão com ícone de folha no `frame_perfil` que abre o popup

    O botão é usado como atalho para chamar `mostrar_mensagem_eco`.

    Parâmetros:
    - frame_perfil: container (tk.Frame) onde o botão será colocado.
    """
    leaf = tk.PhotoImage(file=FILES_PATH + "leaf.png")
    botao_leaf = ttk.Button(
        frame_perfil, image=leaf, bootstyle="sucess-link", command=mostrar_mensagem_eco
    )
    botao_leaf.img = leaf
    botao_leaf.grid(row=1, column=2, sticky="se", pady=(42, 0))


def logoff():
    """Encerra a sessão do usuário atual e retorna à tela de login.

    Limpa o dicionário `contexto.colaborador`, destrói os widgets da janela
    principal e chama `login()` para reiniciar o fluxo de autenticação.
    """
    contexto.colaborador = {}

    for widget in contexto.janela.winfo_children():
        widget.destroy()

    login()


def login():
    """Fluxo de autenticação e inicialização da interface principal.

    Executa a tela de login, obtém os dados do colaborador autenticado e,
    caso exista um usuário, constrói a área superior (`logo_frame`) e
    monta a barra de ferramentas adequada ao cargo (Admin, Coordenador ou
    Professor).

    Efeitos colaterais:
    - Modifica `contexto.janela`, `contexto.frame_conteudo` e cria `logo_frame`.
    - Chama `criar_barra_admin`, `criar_barra_coordenador` ou
      `criar_barra_professor` conforme o cargo.
    """
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
    """Ponto de entrada da aplicação.

    - Verifica variáveis de ambiente e arquivos JSON necessários.
    - Inicializa a janela principal (`contexto.janela`), aplica estilos
      do tema `ttkbootstrap`, configura tamanho e comportamento da janela,
      e inicia o loop principal do Tkinter.
    """
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
        font=(GUI_FONT, 16, "bold"),
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
