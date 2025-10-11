@echo off
echo Instalando uv
pip install uv

echo Ajustando permissões para execução de scripts PowerShell...
powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"

echo Inicializando venv...
.\.venv\Scripts\activate

pause