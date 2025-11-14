# Este arquivo contém as importações e inicializações das interfaces e utilitários do sistema.
# Cada função ou variável importada é descrita abaixo:

from .interface_login import tela_login
from .interface_cadastro_colaborador import iniciar_cadastro
from .alterar_senha_admin import alterar_senha_admin
from .interface_edicao_colaborador import iniciar_edicao_colaborador
from .interface_edicao_turma import iniciar_edicao_turma
from .alterar_senha_colaborador import alterar_senha_colaborador
from .interface_cadastro_turma import iniciar_cadastro_turma
from .interface_cadastro_aluno import iniciar_cadastro_aluno
from .interface_edicao_aluno import iniciar_edicao_aluno
from .interface_atividades_prof import (
    criar_interface_atividades,
    criar_diario,
    criar_interface_frequencia,
)
from .interface_inteligencia import criar_frame_chat
from .utils_tk import limpar_widgets
from .utils_tk import ui_login, ui_geral, encerrar, alt_tamanho_janela

__all__ = [
    # interfaces principais
    "tela_login",
    "iniciar_cadastro",
    "alterar_senha_admin",
    "iniciar_edicao_colaborador",
    "iniciar_edicao_turma",
    "alterar_senha_colaborador",
    "iniciar_cadastro_turma",
    "iniciar_cadastro_aluno",
    "iniciar_edicao_aluno",
    "criar_interface_atividades",
    "criar_diario",
    "criar_interface_frequencia",
    "criar_frame_chat",
    # utilitários
    "ui_login",
    "ui_geral",
    "encerrar",
    "alt_tamanho_janela",
    "limpar_widgets",
]
