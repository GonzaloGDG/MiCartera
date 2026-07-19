"""
routes/cartera.py
Devuelve la cartera del usuario autenticado,
combinando cartera.json con tickers.json.
"""

from fastapi import APIRouter, Query
import json
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_json(filename: str) -> list:
    ruta = os.path.join(BASE_DIR, "..", "data", filename)
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/cartera")
def get_cartera(usuario: str = Query(...)):

    cartera = load_json("cartera.json")
    tickers = {t["ticker"]: t for t in load_json("tickers.json")}

    posiciones = [p for p in cartera if p["usuario"] == usuario]

    resultado = []

    for pos in posiciones:

        ticker_data = tickers.get(pos["ticker"], {})

        precio_actual = ticker_data.get("precio_actual") or 0
        precio_compra = pos["precio_compra"]
        num_titulos = pos["num_titulos"]

        total_actual = round(precio_actual * num_titulos, 2)
        diferencia = round(total_actual - pos["total_invertido"], 2)

        var_compra_pct = round(
            ((precio_actual - precio_compra) / precio_compra * 100)
            if precio_compra else 0,
            2
        )

        resultado.append({
            "ticker": pos["ticker"],
            "nombre": pos["nombre"],
            "num_titulos": num_titulos,
            "precio_compra": precio_compra,
            "precio_actual": precio_actual,
            "variacion_hoy": ticker_data.get("variacion_pct") or 0,
            "variacion_compra": var_compra_pct,
            "total_invertido": pos["total_invertido"],
            "total_actual": total_actual,
            "diferencia": diferencia,
            "moneda": ticker_data.get("moneda", "EUR"),
        })

    return {
        "ok": True,
        "datos": resultado
    }
