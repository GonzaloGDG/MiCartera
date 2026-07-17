
"""
tasks/ticker_updater.py
─────────────────────────────────────────────────────────────────────────────
Tarea de actualización de cotizaciones.

Lee la lista de tickers desde data/tickers.json, obtiene los precios
actuales desde Yahoo Finance y guarda los resultados en el mismo fichero.

Este módulo es independiente de Flask y puede ejecutarse:
  - Manualmente:        python tasks/ticker_updater.py
  - Con un scheduler:   APScheduler, cron, etc.
─────────────────────────────────────────────────────────────────────────────
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from time import sleep
import json
from datetime import datetime, time
from services.yahoo_finance import get_cotizacion


BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
TICKERS_FILE = os.path.join(BASE_DIR, '..', 'data', 'tickers.json')


def load_tickers() -> list:
    """Carga la lista de tickers desde el fichero JSON."""
    with open(TICKERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_tickers(tickers: list) -> None:
    """Guarda la lista de tickers actualizada en el fichero JSON."""
    with open(TICKERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tickers, f, ensure_ascii=False, indent=2)


def actualizar_precios() -> None:
    """
    Recorre todos los tickers del JSON, obtiene su cotización actual
    y actualiza los campos de precio en el mismo fichero.
    """
    tickers = load_tickers()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    actualizados = 0
    errores      = 0

    for entry in tickers:
        ticker = entry['ticker']
        print(f"  → Obteniendo {ticker}...", end=' ')

        resultado = get_cotizacion(ticker)

        if resultado['ok']:
            datos = resultado['datos']
            entry['precio_actual']  = datos.get('precio_actual')
            entry['variacion']      = datos.get('variacion')
            entry['variacion_pct']  = datos.get('variacion_pct')
            entry['precio_cierre']  = datos.get('precio_cierre')
            entry['moneda']         = datos.get('moneda')
            entry['mercado']        = datos.get('mercado')
            entry['sector']         = datos.get('sector')
            entry['max_52s']        = datos.get('max_52s')
            entry['min_52s']        = datos.get('min_52s')
            entry['capitalizacion'] = datos.get('capitalizacion')
            entry['volumen']        = datos.get('volumen')
            entry['ultimo_update']  = timestamp
            print(f"✅ {datos.get('precio_actual')} {datos.get('moneda')}")
            actualizados += 1
        else:
            entry['ultimo_update'] = timestamp
            print(f"❌ Error: {resultado.get('mensaje')}")
            errores += 1
        # ── Delay entre peticiones para evitar rate limit ──
        sleep(1.5)
    save_tickers(tickers)
    print(f"\n✅ Actualización completada — {actualizados} OK / {errores} errores")


if __name__ == '__main__':
    print(f"🔄 Iniciando actualización de precios...")
    actualizar_precios()
