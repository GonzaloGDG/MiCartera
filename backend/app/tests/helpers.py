"""
Funciones auxiliares para los tests de regresión.
"""

from app.services.operaciones_service import (
    borrar_todas_operaciones,
)

from app.services.ahorro_service import (
    borrar_todos_movimientos,
)

from app.services.liquidez_service import (
    establecer_liquidez,
    obtener_importe_liquidez,
)

USUARIO = "pruebas_regresion"


def reset():

    borrar_todas_operaciones(USUARIO)

    borrar_todos_movimientos(USUARIO)

    establecer_liquidez(
        usuario=USUARIO,
        importe=10000,
    )


def liquidez():

    return obtener_importe_liquidez(USUARIO)