"""
Lógica de negocio de la cartera.
"""

from app.repositories.tickers_repository import (
    get_tickers,
)

from app.schemas.cartera import CarteraResponse

from app.services.fifo_service import (
    calcular_posiciones_abiertas,
)


def obtener_cartera(usuario: str):

    posiciones = calcular_posiciones_abiertas(usuario)
    tickers = get_tickers()

    resultado = []
    ultimo_update = None

    for pos in posiciones:

        ticker = tickers.get(pos["ticker"], {})

        if ticker.get("ultimo_update"):
            fecha = ticker["ultimo_update"]

            if ultimo_update is None or fecha > ultimo_update:
                ultimo_update = fecha

        precio_actual = ticker.get("precio_actual") or 0
        precio_compra = pos["precio_medio"]
        num_titulos = pos["titulos"]

        total_actual = round(
            precio_actual * num_titulos,
            2,
        )

        diferencia = round(
            total_actual - pos["coste_total"],
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
            "nombre": ticker.get("nombre", pos["ticker"]),
            "num_titulos": num_titulos,
            "precio_compra": precio_compra,
            "precio_actual": precio_actual,
            "variacion_hoy": ticker.get("variacion_pct", 0),
            "variacion_compra": variacion_compra,
            "total_invertido": pos["coste_total"],
            "total_actual": total_actual,
            "diferencia": diferencia,
            "moneda": ticker.get("moneda", "EUR"),
        })

    return CarteraResponse(
        ok=True,
        datos=resultado,
        ultimo_update=ultimo_update,
    )