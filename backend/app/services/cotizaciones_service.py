"""
Lógica de negocio relacionada con cotizaciones.
"""

from app.providers.yahoo_finance import (
    get_cotizacion,
    get_historico,
)


def obtener_cotizacion(ticker: str):
    return get_cotizacion(ticker)


def obtener_historico(
    ticker: str,
    periodo: str = "1mo",
    intervalo: str = "1d",
):
    return get_historico(
        ticker,
        periodo,
        intervalo,
    )