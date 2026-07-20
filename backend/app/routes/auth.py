"""
Login route for the MiCartera FastAPI application.
"""

from fastapi import APIRouter

from app.repositories.auth_repository import get_usuario

from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
)

router = APIRouter()


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(datos: LoginRequest):

    username = datos.username.strip()
    password = datos.password.strip()

    usuario = get_usuario(username, password)

    if usuario:
        return {
            "ok": True,
            "nombre": usuario["nombre"],
            "rol": usuario["rol"],
        }

    return {
        "ok": False,
        "mensaje": "Usuario o contraseña incorrectos",
    }