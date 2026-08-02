"""
Repositorio de acceso al catálogo de tickers.
"""

from app.repositories.base_repository import load_json

FILENAME = "tickers.json"

def get_tickers():

    tickers = load_json(FILENAME)

    return {
        ticker["ticker"]: ticker
        for ticker in tickers
    }

def validar_ticker(ticker: str):

    tickers = load_json(FILENAME)

    if not any(
        t["ticker"] == ticker
        for t in tickers
    ):
        raise ValueError(
            f"Ticker '{ticker}' no válido."
        )