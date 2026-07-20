"""
services/yahoo_finance.py
─────────────────────────
Servicio de integración con Yahoo Finance.

Contiene las funciones necesarias para obtener cotizaciones
e históricos utilizando la librería yfinance.
"""

import yfinance as yf


def get_cotizacion(ticker: str) -> dict:
    """
    Obtiene la cotización actual de un ticker.
    """
    try:
        accion = yf.Ticker(ticker.upper())
        info = accion.info

        precio_actual = (
            info.get("currentPrice")
            or info.get("regularMarketPrice")
            or info.get("navPrice")
            or 0
        )

        return {
            "ok": True,
            "datos": {
                "ticker": ticker.upper(),
                "nombre": info.get("longName", info.get("shortName", ticker)),
                "precio_actual": precio_actual,
                "precio_apertura": info.get("open"),
                "precio_cierre": info.get("previousClose"),
                "variacion": round(precio_actual - (info.get("previousClose") or 0), 4),
                "variacion_pct": round(info.get("regularMarketChangePercent", 0), 4),
                "moneda": info.get("currency", "USD"),
                "mercado": info.get("exchange", ""),
                "sector": info.get("sector", ""),
                "max_52s": info.get("fiftyTwoWeekHigh"),
                "min_52s": info.get("fiftyTwoWeekLow"),
                "capitalizacion": info.get("marketCap"),
                "volumen": info.get("volume"),
            },
        }

    except Exception as e:
        return {"ok": False, "mensaje": str(e)}


def get_historico(
    ticker: str,
    periodo: str = "1mo",
    intervalo: str = "1d",
) -> dict:
    """
    Obtiene el histórico OHLCV de un ticker.
    """
    try:
        accion = yf.Ticker(ticker.upper())
        hist = accion.history(period=periodo, interval=intervalo)

        if hist.empty:
            return {
                "ok": False,
                "mensaje": "No se encontraron datos históricos",
            }

        registros = []

        for fecha, fila in hist.iterrows():
            registros.append({
                "fecha": fecha.strftime("%Y-%m-%d %H:%M"),
                "open": round(fila["Open"], 4),
                "high": round(fila["High"], 4),
                "low": round(fila["Low"], 4),
                "close": round(fila["Close"], 4),
                "volumen": int(fila["Volume"]),
            })

        return {
            "ok": True,
            "ticker": ticker.upper(),
            "datos": registros,
        }

    except Exception as e:
        return {"ok": False, "mensaje": str(e)}


def get_cotizaciones_multiple(tickers: list) -> list:
    """
    Obtiene la cotización de varios tickers.
    """
    return [get_cotizacion(ticker) for ticker in tickers]