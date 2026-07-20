"""
Lógica de negocio de la cartera.
"""

from app.repositories.cartera_repository import (
    get_cartera_usuario,
    get_tickers,
)

from app.schemas.cartera import CarteraResponse


def obtener_cartera(usuario: str):

    posiciones = get_cartera_usuario(usuario)
    tickers = get_tickers()

    resultado = []

    for pos in posiciones:

        ticker = tickers.get(pos["ticker"], {})

        precio_actual = ticker.get("precio_actual") or 0
        precio_compra = pos["precio_compra"]
        num_titulos = pos["num_titulos"]

        total_actual = round(precio_actual * num_titulos, 2)

        diferencia = round(
            total_actual - pos["total_invertido"],
            2,
        )

        variacion_compra = round(
            (
                (precio_actual - precio_compra)
                / precio_compra
                * 100
            )
            if precio_compra
            else 0,
            2,
        )

        resultado.append({
            "ticker": pos["ticker"],
            "nombre": pos["nombre"],
            "num_titulos": num_titulos,
            "precio_compra": precio_compra,
            "precio_actual": precio_actual,
            "variacion_hoy": ticker.get("variacion_pct", 0),
            "variacion_compra": variacion_compra,
            "total_invertido": pos["total_invertido"],
            "total_actual": total_actual,
            "diferencia": diferencia,
            "moneda": ticker.get("moneda", "EUR"),
        })

    return CarteraResponse(
        ok=True,
        datos=resultado,
    )