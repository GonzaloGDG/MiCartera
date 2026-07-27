"""
Rutas de cotizaciones de MiCartera.
"""

from fastapi import APIRouter
from app.tasks.ticker_updater import actualizar_precios

from app.schemas.cotizaciones import (
    CotizacionResponse,
    HistoricoResponse,
)

from app.services.cotizaciones_service import (
    obtener_cotizacion,
    obtener_historico,
)


router = APIRouter()


@router.get(
    "/cotizacion/{ticker}",
    response_model=CotizacionResponse,
)
def cotizacion(ticker: str):
    return obtener_cotizacion(ticker)


@router.get(
    "/historico/{ticker}",
    response_model=HistoricoResponse,
)
def historico(
    ticker: str,
    periodo: str = "1mo",
    intervalo: str = "1d",
):
    return obtener_historico(
        ticker,
        periodo,
        intervalo,
    )

@router.post("/cotizaciones/actualizar")
def actualizar_cotizaciones():

    return actualizar_precios()