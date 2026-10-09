import pytest

from app.services.liquidez_service import (
    obtener_liquidez,
)

from app.services.ahorro_service import (
    crear_movimiento_ahorro,
    borrar_movimiento_ahorro,
)

from app.services.operaciones_service import (
    crear_operacion,
    borrar_operacion,
)

from app.services.cartera_service import (
    obtener_cartera,
)


USUARIO = "pruebas_regresion"

"Pruebas de regresión"
def test_regresion():

    # Reiniciailizamos el usuario  pruebas de regresión
    reset()
    # Comprobaciones iniciales    
    assert liquidez() == 10000
    