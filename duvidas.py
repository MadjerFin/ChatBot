import anthropic
import os
import dotenv
from prompts import prompt_de_sistema
from google_routes import consultar_rota_google  # ✅ integração com Google Maps

dotenv.load_dotenv()

if not os.environ.get("ANTHROPIC_API_KEY"):
    raise ValueError("ANTHROPIC_API_KEY não encontrada no .env")

modelo = "claude-3-7-sonnet-20250219"
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

    # 🧭 Tenta identificar uma dúvida de rota
    if "como chegar" in prompt_usuario.lower() and " de " in prompt_usuario and " para " in prompt_usuario:
        try:
            partes = prompt_usuario.lower().split(" de ")
            if len(partes) == 2 and " para " in partes[1]:
                origem, destino = partes[1].split(" para ")
                origem = origem.strip()
                destino = destino.strip()

                resposta_google = consultar_rota_google(origem, destino)
                if resposta_google:
                    return f"🧭 Rota sugerida com base no Google Maps:\n\n{resposta_google}"
        except Exception as e:
            print(f"[ERRO ao consultar rota no Google Maps]: {e}")

    # 🤖 Fallback para Anthropic se não for rota ou falhar
    historico.append({
        "role": "user",
        "content": [{"type": "text", "text": prompt_usuario}]
    })

    if len(historico) > 6:
        historico = resumir_historico(historico[-6:])

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))  # criação segura por request

    try:
        message = client.messages.create(
            model=modelo,
            max_tokens=400,
            temperature=0.2,
            system=prompt_de_sistema,
            messages=historico
        )
    except anthropic.APIStatusError as e:
        print(f"[ERRO Anthropic]: {e}")
        return "⚠️ No momento, não foi possível obter resposta da IA. Tente novamente em instantes."

    resposta = message.content[0].text

    historico.append({
        "role": "assistant",
        "content": [{"type": "text", "text": resposta}]
    })

    return resposta
