from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
from duvidas import bot  # sua função de IA
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return redirect("https://trip-red.vercel.app/chatbot")

# 🔹 Webhook que o Twilio chama quando chega msg no WhatsApp
@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    # Pega o texto da msg recebida
    incoming_msg = request.values.get("Body", "").strip()
    # Pega o número do usuário que enviou
    numero_usuario = request.values.get("From", "")

    # Cria resposta no formato Twilio
    resp = MessagingResponse()
    msg = resp.message()

    if not incoming_msg:
        msg.body("Não entendi sua mensagem 🚇")
    else:
        resposta = bot(incoming_msg)  # usa sua IA Trip
        msg.body(resposta)

    # Apenas para log (vai aparecer no terminal)
    print(f"Usuário {numero_usuario} disse: {incoming_msg}")

    return str(resp)

# 🔹 Mantém a rota para o site (Vercel)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "msg" not in data:
        return jsonify({"erro": "Mensagem não fornecida"}), 400
    resposta = bot(data["msg"])
    return jsonify({"resposta": resposta})
