
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

def load_usuarios():
    with open('data/usuarios.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/api/login', methods=['POST'])
def login():
    body = request.get_json()
    username = body.get('username', '').strip()
    password = body.get('password', '').strip()

    usuarios = load_usuarios()
    usuario = next(
        (u for u in usuarios if u['username'] == username and u['password'] == password),
        None
    )

    if usuario:
        return jsonify({
            "ok": True,
            "nombre": usuario['nombre'],
            "rol": usuario['rol']
        })
    else:
        return jsonify({"ok": False, "mensaje": "Usuario o contraseña incorrectos"}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)
