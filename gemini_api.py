from google import genai
from dotenv import get_key
from config import FILES_PATH
import contexto


def enviar_mensagem_gemini(mensagem, anexo):
    client = genai.Client(api_key=get_key(FILES_PATH + ".env", "GEMINI_API_KEY"))

    mensagem = (
        f"(Contexto: Sou o/a {contexto.colaborador['cargo']}/a {contexto.colaborador['nome']}, me ajude com questões pedagógicas e questões de forma sucinta e profissional.)\n\n"
        + mensagem
        + "\n\nAnexo:"
        + str(anexo)
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=mensagem
    )
    return response.text
