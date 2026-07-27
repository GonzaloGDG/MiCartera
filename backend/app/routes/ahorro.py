"""
Rutas relacionadas con el ahorro.
"""

from fastapi import APIRouter

from app.services.ahorro_service import obtener_ahorro
from app.repositories.ahorro_repository import add_movimiento
from app.schemas.ahorro import AhorroResponse


router = APIRouter()


@router.get(
    "/ahorro",
    response_model=AhorroResponse,
)
def ahorro(usuario: str):

    return obtener_ahorro(usuario)


@router.post("/ahorro")
def crear_movimiento(datos: dict):

    movimiento = add_movimiento(
        usuario=datos["usuario"],
        tipo=datos["tipo"],
        importe=datos["importe"],
        fecha=datos["fecha"]
    )

    return {
        "ok": True,
        "datos": movimiento
    }