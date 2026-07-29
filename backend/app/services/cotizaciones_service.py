"""
Lógica de negocio relacionada con cotizaciones.
"""

from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent
TICKERS_FILE = BASE_DIR / "data" / "tickers.json"

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

# ─────────────────────────────────────────────
# ÚLTIMA ACTUALIZACIÓN
# ─────────────────────────────────────────────

def obtener_ultima_actualizacion():

    with open(
        TICKERS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        tickers = json.load(file)

    fechas = [
        ticker.get("ultimo_update")
        for ticker in tickers
        if ticker.get("ultimo_update")
    ]

    if not fechas:
        return None

    return max(fechas)