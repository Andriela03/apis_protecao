from flask import Flask, jsonify, request

app = Flask(__name__)


API_KEY = "MINHA_CHAVE_SECRETA"

@app.route("/hello", methods=["GET"])
def hello():
    chave_recebida = request.headers.get("x-api-key")
    

    if chave_recebida == API_KEY:
        return jsonify({
            "mensagem": "Hello World"
        })
    

    if not chave_recebida:
        status_code = 401
    else:
        status_code = 403
    return jsonify({
        "erro": "Acesso negado. Chave de API inválida ou ausente."
    }), status_code

if __name__ == "__main__":
    app.run(debug=True)
