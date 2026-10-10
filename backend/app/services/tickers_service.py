"""
Lógica de negocio relacionada con el catálogo de tickers.
"""

from app.repositories.tickers_repository import get_tickers


def obtener_tickers():

    return sorted(
        get_tickers().values(),
        key=lambda ticker: ticker["nombre"],
    )