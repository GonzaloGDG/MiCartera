"""
Rutas relacionadas con la liquidez.
"""

from fastapi import APIRouter

from app.schemas.liquidez import ModificarLiquidezRequest
from app.services.liquidez_service import (
    obtener_liquidez,
    establecer_liquidez,
)

router = APIRouter(
    tags=["Liquidez"]
)


@router.get("/liquidez")
def obtener_liquidez_route(usuario: str):

    return {
        "ok": True,
        "importe": obtener_liquidez(usuario),
    }

@router.put("/liquidez")
def modificar_liquidez_route(
    datos: ModificarLiquidezRequest,
):

    return establecer_liquidez(
        usuario=datos.usuario,
        importe=datos.importe,
        moneda=datos.moneda,
    )