"""
Rutas relacionadas con el ahorro.
"""

from fastapi import APIRouter

"Services"
from app.services.ahorro_service import (
    obtener_ahorro,
    crear_movimiento_ahorro,
    borrar_movimiento_ahorro,
    establecer_liquidez,

)
from app.services.liquidez_service import obtener_liquidez


"Schemas"
from app.schemas.ahorro import AhorroResponse
from app.schemas.liquidez import ModificarLiquidezRequest


router = APIRouter()


# ─────────────────────────────────────────────
# OBTENER AHORRO
# ─────────────────────────────────────────────

@router.get(
    "/ahorro",
    response_model=AhorroResponse,
)
def ahorro(usuario: str):

    ahorro_data = obtener_ahorro(usuario)

    liquidez_data = obtener_liquidez(usuario)

    return {
        **ahorro_data,
        "liquidez": liquidez_data["total"]
    }


# ─────────────────────────────────────────────
# CREAR MOVIMIENTO
# ─────────────────────────────────────────────

@router.post("/ahorro")
def crear_movimiento(datos: dict):

    resultado = crear_movimiento_ahorro(
        usuario=datos["usuario"],
        tipo=datos["tipo"],
        importe=datos["importe"],
        fecha=datos["fecha"],
    )

    return {
        "ok": True,
        "datos": resultado["movimiento"],
        "liquidez": resultado["liquidez"],
    }

@router.delete("/ahorro/{movimiento_id}")
def borrar_movimiento(
    movimiento_id: int,
    usuario: str
):

    movimiento = borrar_movimiento_ahorro(
        usuario=usuario,
        movimiento_id=movimiento_id
    )

    return {
        "ok": True,
        "datos": movimiento
    }

@router.put("/liquidez")
def actualizar_liquidez(datos: ModificarLiquidezRequest):

    resultado = establecer_liquidez(
        usuario=datos.usuario,
        importe=datos.importe,
        moneda=datos.moneda,
    )

    return resultado