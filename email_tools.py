import smtplib
from seguranca import get_env_key
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
USERNAME = "EduSmarthelper@gmail.com"
PASSWORD = get_env_key("EMAIL_PASSWORD")

usuario = {"nome": "Vitor Angelo", "email": "vitorcincerre@hotmail.com"}
senha = "123456"


def novo_email(usuario: dict, senha: str) -> None:
    """_summary_

    Args:
        usuario (dict): {'nome': 'Name', 'email': 'email@domain.com'}
        senha (str): senha123
    """
    corpo = f"""    Olá {usuario['nome']},\n\nAtendendo a solicitação de redefinição de sua senha, estamos enviando este email para informar sua nova senha provisória no sistema EduSmart.
Favor realizar o seu login na plataforma e alterar sua senha.
    
{senha}
    
Qualquer dúvida, favor contatar o responsável pela sua organização."""
    mensagem = MIMEText(corpo, "plain")
    mensagem["Subject"] = "EduSmart - Nova senha de acesso"
    mensagem["From"] = USERNAME
    mensagem["To"] = usuario["email"]

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(USERNAME, PASSWORD)
        print(server.sendmail(USERNAME, usuario["email"], mensagem.as_string()))


if __name__ == "__main__":
    novo_email(usuario, senha)
