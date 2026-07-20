"""
Repositorio de acceso a usuarios.

Actualmente lee los datos desde usuarios.json.
En el futuro leerá desde PostgreSQL sin cambiar
el resto de la aplicación.
"""

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
USUARIOS_FILE = BASE_DIR / "data" / "usuarios.json"


def load_usuarios() -> list:
    """Carga todos los usuarios."""

    with open(USUARIOS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_usuario(username: str, password: str):

    usuarios = load_usuarios()

    return next(
        (
            usuario
            for usuario in usuarios
            if usuario["username"] == username
            and usuario["password"] == password
        ),
        None,
    )