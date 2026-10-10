from app.schemas.operaciones import OperacionCreateRequest
from app.services.ahorro_service import crear_movimiento_ahorro
from app.services.operaciones_service import (
    borrar_operacion,
    crear_operacion,
)
from app.tests.helpers import USUARIO, liquidez, reset


"Pruebas de regresión"
def test_regresion():

    reset()

    assert liquidez() == 10000

    movimiento = crear_movimiento_ahorro(
        usuario=USUARIO,
        tipo="ingreso",
        importe=500,
        fecha="2025-01-01",
    )

    assert movimiento["movimiento"]["tipo"] == "ingreso"
    assert liquidez() == 10500

    operacion = crear_operacion(
        OperacionCreateRequest(
            usuario=USUARIO,
            tipo="compra",
            ticker="ANA.MC",
            fecha="2025-01-02",
            titulos=10,
            precio=100,
            comision=5,
        )
    )

    assert operacion["ticker"] == "ANA.MC"
    assert liquidez() == 9495

    operacion_borrada = borrar_operacion(
        usuario=USUARIO,
        operacion_id=operacion["id"],
    )

    assert operacion_borrada["id"] == operacion["id"]
    assert liquidez() == 10500
    