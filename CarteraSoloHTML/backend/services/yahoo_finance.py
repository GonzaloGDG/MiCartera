
"""
services/yahoo_finance.py
─────────────────────────
Servicio de integración con Yahoo Finance.
Proporciona funciones para obtener cotizaciones
y datos históricos de activos financieros.
"""
import ssl
import urllib3
import yfinance as yf
from curl_cffi import requests as curl_requests


# ── Bypass SSL corporativo (solo desarrollo) ──────────
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Sesión curl_cffi sin verificación SSL (compatible con yfinance moderno)
_session = curl_requests.Session(verify=False)

def get_cotizacion(ticker: str) -> dict:
    """
    Obtiene los datos de cotización actuales de un ticker.
    """
    try:
        accion = yf.Ticker(ticker.upper(), session=_session)
        info   = accion.info

        precio_actual = (
            info.get('currentPrice') or
            info.get('regularMarketPrice') or
            info.get('navPrice') or
            0
        )

        return {
            "ok": True,
            "datos": {
                "ticker":          ticker.upper(),
                "nombre":          info.get('longName', info.get('shortName', ticker)),
                "precio_actual":   precio_actual,
                "precio_apertura": info.get('open'),
                "precio_cierre":   info.get('previousClose'),
                "variacion":       round(precio_actual - (info.get('previousClose') or 0), 4),
                "variacion_pct":   round(info.get('regularMarketChangePercent', 0), 4),
                "moneda":          info.get('currency', 'USD'),
                "mercado":         info.get('exchange', ''),
                "sector":          info.get('sector', ''),
                "max_52s":         info.get('fiftyTwoWeekHigh'),
                "min_52s":         info.get('fiftyTwoWeekLow'),
                "capitalizacion":  info.get('marketCap'),
                "volumen":         info.get('volume'),
            }
        }
    except Exception as e:
        return {"ok": False, "mensaje": str(e)}


def get_historico(ticker: str, periodo: str = '1mo', intervalo: str = '1d') -> dict:
    """
    Obtiene el histórico de precios OHLCV de un ticker.
    """
    try:
        accion = yf.Ticker(ticker.upper())
        hist   = accion.history(period=periodo, interval=intervalo)

        if hist.empty:
            return {"ok": False, "mensaje": "No se encontraron datos históricos"}

        registros = []
        for fecha, fila in hist.iterrows():
            registros.append({
                "fecha":   fecha.strftime('%Y-%m-%d %H:%M'),
                "open":    round(fila['Open'], 4),
                "high":    round(fila['High'], 4),
                "low":     round(fila['Low'], 4),
                "close":   round(fila['Close'], 4),
                "volumen": int(fila['Volume'])
            })

        return {"ok": True, "ticker": ticker.upper(), "datos": registros}

    except Exception as e:
        return {"ok": False, "mensaje": str(e)}


def get_cotizaciones_multiple(tickers: list) -> list:
    """
    Obtiene la cotización actual de una lista de tickers en una sola llamada.
    """
    return [get_cotizacion(t) for t in tickers]
