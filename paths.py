"""Configura caminhos usados pela aplicação.

Este módulo define o caminho para o diretório de arquivos da aplicação e
garante que o diretório exista no sistema de arquivos. É utilizado por
outros módulos para ler/escrever arquivos (JSON, imagens, etc.).
"""

from os import path, mkdir

# Caminho relativo para a pasta que armazena arquivos da aplicação
FILES_PATH = "./files/"

if not path.exists(FILES_PATH):
    mkdir(FILES_PATH)
