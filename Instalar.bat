@echo off
echo Instalando uv
pip install uv

echo Ajustando permissões para execução de scripts PowerShell...
powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"

echo Sincronizando dependencias...
.\.venv\Scripts\uv.exe sync

echo.
echo Executando o sistema...
.\.venv\Scripts\pythonw.exe interface.py

pause