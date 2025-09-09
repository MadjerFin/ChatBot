from flask import Flask, request, redirect, jsonify
from duvidas import bot  # sua função de IA
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

# 🔹 Página inicial do site
@app.route("/", methods=["GET"])
def home():
    return redirect("https://trip-red.vercel.app/chatbot")

# 🔹 Webhook do Twilio para WhatsApp
@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    print("Webhook chamado")  # confirma que o Twilio chegou aqui
    print("Request values:", request.values)  # mostra todos os dados recebidos

    incoming_msg = request.values.get("Body", "").strip()
    numero_usuario = request.values.get("From", "")

    resp = MessagingResponse()
    msg = resp.message()

    if not incoming_msg:
        msg.body("Não entendi sua mensagem 🚇")
    else:
        try:
            resposta = bot(incoming_msg)  # chama a IA
            msg.body(resposta)
        except Exception as e:
            print("Erro no bot:", e)
            msg.body("Ops, erro interno 🤖")

    print(f"Usuário {numero_usuario} disse: {incoming_msg}")
    return str(resp), 200, {"Content-Type": "application/xml"}

# 🔹 Rota para chat via frontend (opcional)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "msg" not in data:
        return jsonify({"erro": "Mensagem não fornecida"}), 400
    try:
        resposta = bot(data["msg"])
    except Exception as e:
        print("Erro no bot via /chat:", e)
        return jsonify({"erro": "Erro interno"}), 500
    return jsonify({"resposta": resposta})

# 🔹 Start do Flask no Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
