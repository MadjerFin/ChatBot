from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
from duvidas import bot, limpar_historico

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return redirect("https://trip-red.vercel.app/chatbot")

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json.get("msg")
    if not prompt:
        return jsonify({"erro": "Mensagem não fornecida"}), 400
    resposta = bot(prompt)
    return jsonify({"resposta": resposta})

@app.route("/limpar_historico", methods=["POST"])
def limpar_historico_route():
    limpar_historico()
    return jsonify({"status": "Histórico limpo"})

if __name__ == "__main__":
    app.run(debug=True)
