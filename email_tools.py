import smtplib
from seguranca import get_env_key
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
USERNAME = "smarteduhelper@gmail.com"
PASSWORD = get_env_key("EMAIL_PASSWORD")

usuario = {"nome": "Vitor Angelo", "email": "vitorcincerre@gmail.com"}
senha = "123456"


def novo_email(usuario: dict, senha: str):
    corpo = f"""    Olá {usuario['nome']},\n\nEstamos enviando este email para informar sua
nova senha provisória no sistema SmartEdu.
    Favor realizar o seu login na plataforma e alterar sua senha.
    
    {senha}
    
    Qualquer dúvida, favor contatar o responsável pela sua organização."""
    mensagem = MIMEText(corpo, "plain")
    mensagem["Subject"] = "SmartEdu - Nova senha de acesso"
    mensagem["From"] = USERNAME
    mensagem["To"] = usuario["email"]

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, usuario["email"], mensagem.as_string())
