"""
Rutas relacionadas con el ahorro.
"""

from fastapi import APIRouter, HTTPException

"Services"
from app.services.ahorro_service import (
    obtener_ahorro,
    crear_movimiento_ahorro,
    borrar_movimiento_ahorro,
    

)
from app.services.liquidez_service import (
    obtener_liquidez,
    establecer_liquidez,
)

"Schemas"
from app.schemas.ahorro import AhorroResponse
from app.schemas.liquidez import ModificarLiquidezRequest


router = APIRouter(
    tags=["Ahorro"]
)

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

    try:
        resultado = crear_movimiento_ahorro(
            usuario=datos["usuario"],
            tipo=datos["tipo"],
            importe=datos["importe"],
            fecha=datos["fecha"],
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

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

    try:
        movimiento = borrar_movimiento_ahorro(
            usuario=usuario,
            movimiento_id=movimiento_id
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return {
        "ok": True,
        "datos": movimiento
    }