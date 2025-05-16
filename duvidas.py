import anthropic
import os
import dotenv
from prompts import prompt_de_sistema

dotenv.load_dotenv()
print("Chave carregada:", os.environ.get("ANTHROPIC_API_KEY"))
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)
modelo = "claude-3-7-sonnet-20250219"

# Histórico começa vazio
historico = []

def resumir_historico(historico):
    """
    Função opcional para resumir histórico se necessário.
    Aqui ele apenas retorna uma versão simples,
    mas você poderia chamar a própria API pra gerar um resumo bonito.
    """
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

    # Adiciona a nova pergunta ao histórico
    historico.append({
        "role": "user",
        "content": [{"type": "text", "text": prompt_usuario}]
    })

    # Se o histórico ficar muito grande, resumir as mensagens antigas
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

    # Adiciona a resposta do bot ao histórico
    historico.append({
        "role": "assistant",
        "content": [{"type": "text", "text": resposta}]
    })

    return resposta
