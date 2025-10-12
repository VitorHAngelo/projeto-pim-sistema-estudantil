@echo off
echo Instalando uv
pip install uv

cls
echo Ajustando permissoes para execucao de scripts PowerShell...
powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"

cls
IF NOT EXIST ".venv" (
    echo Criando ambiente virtual...
    uv venv
) ELSE (
    echo Ambiente virtual já existe.
)

cls
echo Sincronizando dependencias...
uv sync

cls
echo Ambiente instalado e preparado
pause