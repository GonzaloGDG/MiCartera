"""
Login route for the MiCartera FastAPI application.
This route handles user authentication by verifying
the provided username and password.
"""

from fastapi import APIRouter
from pydantic import BaseModel
import json
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class LoginRequest(BaseModel):
    username: str
    password: str


def load_usuarios():
    ruta = os.path.join(BASE_DIR, "..", "data", "usuarios.json")
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


@router.post("/login")
def login(datos: LoginRequest):

    username = datos.username.strip()
    password = datos.password.strip()

    usuarios = load_usuarios()

    usuario = next(
        (
            u for u in usuarios
            if u["username"] == username
            and u["password"] == password
        ),
        None
    )

    if usuario:
        return {
            "ok": True,
            "nombre": usuario["nombre"],
            "rol": usuario["rol"]
        }

    return {
        "ok": False,
        "mensaje": "Usuario o contraseña incorrectos"
    }