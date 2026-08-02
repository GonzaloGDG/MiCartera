"""
Lógica FIFO (First In, First Out).

Calcula las posiciones abiertas de cada valor.
"""

from collections import defaultdict

from app.repositories.operaciones_repository import (
    obtener_operaciones,
)


def calcular_posiciones_abiertas(usuario: str):

    operaciones = obtener_operaciones(usuario)

    operaciones.sort(
        key=lambda op: (
            op["fecha"],
            op["id"],
        )
    )

    # Cola FIFO de compras abiertas
    posiciones = defaultdict(list)

    for operacion in operaciones:

        if operacion["tipo"] == "compra":

            posiciones[operacion["ticker"]].append(
                {
                    "titulos": operacion["titulos"],
                    "coste_adquisicion": (
                        operacion["titulos"]
                        * operacion["precio"]
                        + operacion["comision"]
                    ),
                }
            )

        elif operacion["tipo"] == "venta":

            pendientes = operacion["titulos"]

            lotes = posiciones[operacion["ticker"]]

            while pendientes > 0:

                if not lotes:
                    raise ValueError(
                        f"No hay títulos disponibles de {operacion['ticker']}"
                    )

                lote = lotes[0]

                if lote["titulos"] > pendientes:

                    titulos_originales = lote["titulos"]

                    proporcion = (
                        pendientes / titulos_originales
                    )

                    coste_vendido = (
                        lote["coste_adquisicion"] * proporcion
                    )

                    lote["titulos"] -= pendientes
                    lote["coste_adquisicion"] -= coste_vendido

                    pendientes = 0

                else:

                    pendientes -= lote["titulos"]

                    lotes.pop(0)

    resultado = []

    for ticker, lotes in posiciones.items():

        titulos = sum(
            lote["titulos"]
            for lote in lotes
        )

        if titulos == 0:
            continue

        coste_total = sum(
            lote["coste_adquisicion"]
            for lote in lotes
        )

        precio_medio = (
            coste_total / titulos
        )

        resultado.append(
            {
                "ticker": ticker,
                "titulos": titulos,
                "coste_total": coste_total,
                "precio_medio": precio_medio,
            }
        )

    return resultado