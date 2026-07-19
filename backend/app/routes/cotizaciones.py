"""
Rutas de cotizaciones.
La lógica de negocio está en services/yahoo_finance.py
"""

from fastapi import APIRouter, Query

from app.services.yahoo_finance import (
    get_cotizacion,
    get_historico,
)

router = APIRouter()


@router.get("/cotizacion/{ticker}")
def cotizacion(ticker: str):

    resultado = get_cotizacion(ticker)

    return resultado


@router.get("/historico/{ticker}")
def historico(
    ticker: str,
    periodo: str = Query("1mo"),
    intervalo: str = Query("1d")
):

    resultado = get_historico(
        ticker,
        periodo,
        intervalo
    )

    return resultado