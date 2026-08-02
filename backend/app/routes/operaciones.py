"""
Rutas relacionadas con las operaciones de cartera.
"""

from fastapi import APIRouter
from fastapi import HTTPException

from app.schemas.operaciones import OperacionCreateRequest
from app.services.operaciones_service import (
    crear_operacion,
    get_operaciones_usuario,
    borrar_operacion,
)

router = APIRouter(
    tags=["Operaciones"]
)

@router.post("/operaciones")
def crear_operacion_route(datos: OperacionCreateRequest):

    try:

        operacion = crear_operacion(datos)

        return {
            "ok": True,
            "datos": operacion
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

        
@router.get("/operaciones")
def listar_operaciones(usuario: str):

    return get_operaciones_usuario(usuario)

@router.delete("/operaciones/{operacion_id}")
def borrar_operacion_route(
    usuario: str,
    operacion_id: int,
):

    try:

        operacion = borrar_operacion(
            usuario,
            operacion_id,
        )

        return {
            "ok": True,
            "datos": operacion,
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )