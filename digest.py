from flask import Flask
from flask_httpauth import HTTPDigestAuth

app = Flask(__name__)
app.secret_key = 'chave-secreta-digest'

auth = HTTPDigestAuth(realm="hello")

USERS = {
    "admin": "123"
}

@auth.get_password
def get_password(username):
    return USERS.get(username)

@app.route('/hello', methods = ["GET"])
@auth.login_required
def hello():
    return f'Olá, {auth.current_user()}!'

if __name__ == '__main__':
    app.run(debug=True)