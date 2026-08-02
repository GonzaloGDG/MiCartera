"""
Lógica de negocio relacionada con el catálogo de tickers.
"""

from app.repositories.tickers_repository import get_tickers


def obtener_tickers():

    tickers = get_tickers()

    tickers.sort(
        key=lambda ticker: ticker["nombre"]
    )

    return tickers