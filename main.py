from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
from duvidas import bot  # sua função de IA
import os
import threading
import time
from whatsapp_client import WhatsAppClient

app = Flask(__name__)

# 🔹 Ativa CORS para todas as rotas ou apenas para o frontend do Vercel
CORS(app, origins=["https://trip-red.vercel.app"])

# 🔹 Cliente WhatsApp (usando Selenium + WhatsApp Web)
whatsapp = None
whatsapp_ready = False

def iniciar_whatsapp():
    """Inicializa o cliente WhatsApp em uma thread separada"""
    global whatsapp, whatsapp_ready
    try:
        print("🚀 Iniciando cliente WhatsApp...")
        whatsapp = WhatsAppClient()
        whatsapp.iniciar()
        whatsapp_ready = True
        print("✅ WhatsApp conectado e pronto!")

        # Loop para processar mensagens
        whatsapp.processar_mensagens(callback=processar_mensagem_whatsapp)
    except Exception as e:
        print(f"❌ Erro ao iniciar WhatsApp: {e}")
        whatsapp_ready = False

def processar_mensagem_whatsapp(numero, mensagem):
    """Processa mensagens recebidas do WhatsApp"""
    print(f"📱 Mensagem de {numero}: {mensagem}")

    try:
        resposta = bot(mensagem)
        whatsapp.enviar_mensagem(numero, resposta)
        print(f"✅ Resposta enviada para {numero}")
    except Exception as e:
        print(f"❌ Erro ao processar mensagem: {e}")
        whatsapp.enviar_mensagem(numero, "Ops, erro interno 🤖")

# 🔹 Página inicial do site
@app.route("/", methods=["GET"])
def home():
    return redirect("https://trip-red.vercel.app/chatbot")

# 🔹 Endpoint para verificar status do WhatsApp
@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "whatsapp_conectado": whatsapp_ready,
        "servidor": "online"
    })

# 🔹 Rota para chat via frontend
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

# 🔹 Endpoint opcional para enviar mensagem manualmente (teste)
@app.route("/enviar", methods=["POST"])
def enviar_mensagem():
    if not whatsapp_ready:
        return jsonify({"erro": "WhatsApp não conectado"}), 503

    data = request.get_json()
    numero = data.get("numero")
    mensagem = data.get("mensagem")

    if not numero or not mensagem:
        return jsonify({"erro": "Número e mensagem são obrigatórios"}), 400

    try:
        whatsapp.enviar_mensagem(numero, mensagem)
        return jsonify({"status": "enviado"})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    # Inicia o WhatsApp em uma thread separada
    whatsapp_thread = threading.Thread(target=iniciar_whatsapp, daemon=True)
    whatsapp_thread.start()

    # Aguarda alguns segundos para o WhatsApp inicializar
    print("⏳ Aguardando WhatsApp inicializar...")
    time.sleep(5)

    # Inicia o servidor Flask
    print("🌐 Iniciando servidor Flask...")
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)
