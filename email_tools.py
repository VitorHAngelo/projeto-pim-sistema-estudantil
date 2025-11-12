"""Utilitários para envio de email a partir do sistema.

Contém helper para enviar email de redefinição de senha usando SMTP. O
arquivo obtém a senha do remetente a partir do arquivo `.env` via
`seguranca.get_env_key`.
"""

import smtplib
from seguranca import get_env_key
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
USERNAME = "EduSmarthelper@gmail.com"
PASSWORD = get_env_key("EMAIL_PASSWORD")


def novo_email(usuario: dict, senha: str) -> None:
    """Envia um email de notificação com uma senha provisória.

    Parâmetros:
    - usuario (dict): dicionário com chaves 'nome' e 'email'.
    - senha (str): senha provisória a ser enviada no corpo do email.

    O email é enviado por SMTP para o endereço informado em `usuario['email']`.
    Não retorna valor. Em caso de falha de envio, a exceção do smtplib será
    propagada para o chamador.
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
    usuario = {"nome": "Vitor Angelo", "email": "vitorcincerre@hotmail.com"}
    senha = "123456"
    novo_email(usuario, senha)
