"""Integração simples com a API Gemini (Google GenAI).

Este módulo encapsula a chamada ao cliente GenAI, adicionando um cabeçalho
de contexto com o cargo/nome do colaborador atual (armazenado em
`contexto.colaborador`) antes de enviar a mensagem.
"""

from google import genai
from dotenv import get_key
from config import FILES_PATH
import contexto


def enviar_mensagem_gemini(mensagem, anexo):
    """Envia `mensagem` à API Gemini e retorna o texto de resposta.

    Parâmetros:
    - mensagem (str): texto que será enviado ao modelo.
    - anexo (qualquer): dados adicionais (lista, dicionário, etc.) que serão
      concatenados ao contexto da mensagem.

    O texto enviado ao modelo é prefixado com informações sobre o cargo e
    o nome do usuário atualmente em `contexto.colaborador` para orientar a
    geração. Retorna o texto da resposta retornada pelo cliente GenAI.
    """
    try:
        client = genai.Client(api_key=get_key(FILES_PATH + ".env", "GEMINI_API_KEY"))

        mensagem_com_contexto = (
            f"(Contexto: Sou o/a {contexto.colaborador['cargo']}/a {contexto.colaborador['nome']}, me ajude com questões pedagógicas e questões de forma sucinta e profissional.)\n\n"
            + mensagem
            + "\n\nAnexo:"
            + str(anexo)
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=mensagem_com_contexto
        )

        if hasattr(response, "text") and response.text.strip():
            return response.text.strip()
        else:
            return "⚠️ Não foi possível obter uma resposta da IA. Tente novamente."

    except Exception as e:
        return f"❌ Erro ao comunicar com o serviço: {e}"
