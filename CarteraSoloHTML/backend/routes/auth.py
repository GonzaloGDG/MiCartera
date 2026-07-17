"""
    Login route for the Flask application. 
    This route handles user authentication by verifying 
    the provided username and password 
"""
from flask import Blueprint, jsonify, request
import json, os

auth_bp = Blueprint('auth', __name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_usuarios():
    ruta = os.path.join(BASE_DIR, '..', 'data', 'usuarios.json')
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

@auth_bp.route('/login', methods=['POST'])
def login():
    body     = request.get_json()
    username = body.get('username', '').strip()
    password = body.get('password', '').strip()

    usuarios = load_usuarios()
    usuario  = next(
        (u for u in usuarios if u['username'] == username and u['password'] == password),
        None
    )

    if usuario:
        return jsonify({"ok": True, "nombre": usuario['nombre'], "rol": usuario['rol']})
    else:
        return jsonify({"ok": False, "mensaje": "Usuario o contraseña incorrectos"}), 401
