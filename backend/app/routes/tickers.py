"""
Rutas relacionadas con el catálogo de tickers.
"""

from fastapi import APIRouter

from app.services.tickers_service import (
    obtener_tickers,
)

router = APIRouter(
    tags=["Tickers"]
)


@router.get("/tickers")
def listar_tickers():

    return {
        "ok": True,
        "datos": obtener_tickers()
    }