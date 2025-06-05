import anthropic
import os
import dotenv
from prompts import prompt_de_sistema

dotenv.load_dotenv()

if not os.environ.get("ANTHROPIC_API_KEY"):
    raise ValueError("ANTHROPIC_API_KEY não encontrada no .env")

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

modelo = "claude-sonnet-4-20250514"
historico = []

def resumir_historico(historico):
    textos = []
    for msg in historico:
        if msg["role"] == "user":
            textos.append(f"Usuário: {msg['content'][0]['text']}")
        elif msg["role"] == "assistant":
            textos.append(f"Assistente: {msg['content'][0]['text']}")
    resumo = "\n".join(textos)
    return [{
        "role": "user",
        "content": [{"type": "text", "text": f"Resumo da conversa até aqui:\n{resumo}"}]
    }]

def bot(prompt_usuario):
    global historico

    historico.append({
        "role": "user",
        "content": [{"type": "text", "text": prompt_usuario}]
    })

    if len(historico) > 6:
        historico = resumir_historico(historico[-6:])

    message = client.messages.create(
        model=modelo,
        max_tokens=400,
        temperature=0.2,
        system=prompt_de_sistema,
        messages=historico
    )

    resposta = message.content[0].text

    historico.append({
        "role": "assistant",
        "content": [{"type": "text", "text": resposta}]
    })

    return resposta
