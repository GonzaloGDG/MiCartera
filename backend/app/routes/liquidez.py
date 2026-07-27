"""
Rutas relacionadas con la liquidez.
"""

from fastapi import APIRouter

from app.services.liquidez_service import obtener_liquidez
from app.schemas.liquidez import LiquidezResponse


router = APIRouter()


@router.get(
    "/liquidez",
    response_model=LiquidezResponse,
)
def liquidez(usuario: str):

    return obtener_liquidez(usuario)