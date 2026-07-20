"""
routes/cartera.py
"""

from fastapi import APIRouter

from app.services.cartera_service import obtener_cartera
from app.schemas.cartera import CarteraResponse

router = APIRouter()


@router.get(
    "/cartera",
    response_model=CarteraResponse,
)
def cartera(usuario: str):

    return obtener_cartera(usuario)