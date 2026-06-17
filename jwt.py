import os
import sys
path_original = list(sys.path)

# Remove o diretório atual do sys.path para permitir a importação do pacote 'jwt' (PyJWT)
diretorio_script = os.path.dirname(os.path.abspath(__file__))
if diretorio_script in sys.path:
    sys.path.remove(diretorio_script)

try:
    import jwt
    import datetime
finally:
    # Restaura o path original
    sys.path[:] = path_original

from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'


USUARIO_CORRETO = "admin"
SENHA_CORRETA = "123"

@app.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    
    if not dados or not dados.get("username") or not dados.get("password"):
        return jsonify({"erro": "Usuário e senha são obrigatórios"}), 400
        
    if dados.get("username") == USUARIO_CORRETO and dados.get("password") == SENHA_CORRETA:
    
        payload = {
            "user": USUARIO_CORRETO,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({"access_token": token})
    
    return jsonify({"erro": "Credenciais inválidas"}), 401

@app.route("/hello", methods=["GET"])
def hello():
    # Obtém o token do cabeçalho Authorization
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        return jsonify({"erro": "Token ausente"}), 401
    
    try:
        # Formato esperado: "Bearer <token>"
        partes = auth_header.split(" ")
        if len(partes) != 2 or partes[0] != "Bearer":
            return jsonify({"erro": "Formato de token inválido. Use 'Bearer <token>'"}), 401
            
        token = partes[1]
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return jsonify({
            "mensagem": "Hello World",
            "usuario": payload["user"]
        })
    except jwt.ExpiredSignatureError:
        return jsonify({"erro": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"erro": "Token inválido"}), 401

if __name__ == "__main__":
    app.run(debug=True)
