from flask import Flask, request, redirect, send_from_directory
from flask_cors import CORS
from duvidas import bot

app = Flask(__name__)
CORS(app)

# Redireciona para a rota do front-end
@app.route("/")
def home():
    return redirect("http://localhost:3000/chatbot")  # ou outra rota Next.js que desejar

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    resposta = bot(prompt)
    return resposta

@app.route("/limpar_historico", methods=["POST"])
def limpar_historico():
    return "Histórico limpo"

if __name__ == "__main__":
    app.run(debug=True)
