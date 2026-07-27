"""
Lógica de negocio del ahorro.
"""

from app.repositories.ahorro_repository import (
    get_movimientos_usuario,
)


def obtener_ahorro(usuario: str):

    movimientos = get_movimientos_usuario(usuario)

    # Ordenar movimientos del más reciente al más antiguo
    movimientos = sorted(
        movimientos,
        key=lambda movimiento: movimiento["fecha"],
        reverse=True,
    )

    # Total neto histórico
    total_neto = 0

    # Totales por año
    totales_anuales = {}

    for movimiento in movimientos:

        importe = movimiento["importe"]
        tipo = movimiento["tipo"]
        fecha = movimiento["fecha"]

        # Ingresos suman
        if tipo == "ingreso":
            importe_neto = importe

        # Retiradas restan
        elif tipo == "retirada":
            importe_neto = -importe

        else:
            continue

        total_neto += importe_neto

        # Obtener año
        año = fecha[:4]

        if año not in totales_anuales:
            totales_anuales[año] = 0

        totales_anuales[año] += importe_neto

    return {
        "ok": True,
        "datos": movimientos,
        "total_neto": round(total_neto, 2),
        "totales_anuales": totales_anuales,
    }