from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
from duvidas import bot

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return redirect("https://trip-red.vercel.app/chatbot")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "msg" not in data:
        return jsonify({"erro": "Mensagem não fornecida"}), 400
    resposta = bot(data["msg"])
    return jsonify({"resposta": resposta})

# Não inclua app.run aqui para ambientes como Render (usa gunicorn)
