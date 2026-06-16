from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

USUARIO = "admin"
SENHA = "123"

@auth.verify_password
def verify_password(username, password):
    return username == USUARIO and password == SENHA

@app.route("/hello", methods=["GET"])
@auth.login_required
def hello():
    return jsonify({
        "mensagem": "Hello World"
    })

if __name__ == "__main__":
    app.run(debug=True)