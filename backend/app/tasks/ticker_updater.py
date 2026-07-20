"""
app/tasks/ticker_updater.py
────────────────────────────────────────────────────────────
Actualiza las cotizaciones almacenadas en data/tickers.json.

Puede ejecutarse manualmente:

    python -m app.tasks.ticker_updater

Más adelante podrá ejecutarse mediante un scheduler.
────────────────────────────────────────────────────────────
"""

import json
import os
from datetime import datetime
from time import sleep

from app.services.yahoo_finance import get_cotizacion

# Tiempo de espera entre peticiones a Yahoo
REQUEST_DELAY = 1.5

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TICKERS_FILE = os.path.join(BASE_DIR, "..", "data", "tickers.json")


def load_tickers() -> list:
    """Carga los tickers desde el fichero JSON."""
    with open(TICKERS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_tickers(tickers: list) -> None:
    """Guarda los tickers actualizados."""
    with open(TICKERS_FILE, "w", encoding="utf-8") as file:
        json.dump(tickers, file, ensure_ascii=False, indent=2)


def actualizar_precios() -> None:
    """Actualiza todas las cotizaciones."""

    tickers = load_tickers()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    actualizados = 0
    errores = 0

    for entry in tickers:

        ticker = entry["ticker"]

        print(f"→ Obteniendo {ticker}...", end=" ")

        resultado = get_cotizacion(ticker)

        if resultado["ok"]:

            datos = resultado["datos"]

            entry["precio_actual"] = datos.get("precio_actual")
            entry["variacion"] = datos.get("variacion")
            entry["variacion_pct"] = datos.get("variacion_pct")
            entry["precio_cierre"] = datos.get("precio_cierre")
            entry["moneda"] = datos.get("moneda")
            entry["mercado"] = datos.get("mercado")
            entry["sector"] = datos.get("sector")
            entry["max_52s"] = datos.get("max_52s")
            entry["min_52s"] = datos.get("min_52s")
            entry["capitalizacion"] = datos.get("capitalizacion")
            entry["volumen"] = datos.get("volumen")
            entry["ultimo_update"] = timestamp

            print(f"✅ {datos.get('precio_actual')} {datos.get('moneda')}")
            actualizados += 1

        else:

            entry["ultimo_update"] = timestamp

            print(f"❌ {resultado.get('mensaje')}")
            errores += 1

        sleep(REQUEST_DELAY)

    save_tickers(tickers)

    print("\n────────────────────────────────────")
    print(f"Actualizados : {actualizados}")
    print(f"Errores      : {errores}")
    print("Proceso finalizado.")
    print("────────────────────────────────────")


def main() -> None:
    """Punto de entrada del script."""

    print("🔄 Iniciando actualización de cotizaciones...\n")
    actualizar_precios()


if __name__ == "__main__":
    main()