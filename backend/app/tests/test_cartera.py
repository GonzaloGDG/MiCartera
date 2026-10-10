import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.operaciones_repository import add_operacion
from app.schemas.operaciones import OperacionCreateRequest
from app.services.cartera_service import obtener_cartera
from app.services.fifo_service import calcular_posiciones_abiertas
from app.services.operaciones_service import crear_operacion


def crear_operacion_cartera(tipo, titulos, precio, fecha, comision=0):
    return crear_operacion(
        OperacionCreateRequest(
            usuario="pruebas_regresion",
            tipo=tipo,
            ticker="ANA.MC",
            fecha=fecha,
            titulos=titulos,
            precio=precio,
            comision=comision,
        )
    )


def test_fifo_conserva_el_coste_del_lote_parcialmente_abierto():
    crear_operacion_cartera("compra", 10, 100, "2025-01-01", 10)
    crear_operacion_cartera("compra", 10, 200, "2025-02-01", 10)
    crear_operacion_cartera("venta", 15, 150, "2025-03-01", 5)

    posiciones = calcular_posiciones_abiertas("pruebas_regresion")

    assert posiciones == [
        {
            "ticker": "ANA.MC",
            "titulos": 5,
            "coste_total": pytest.approx(1005),
            "precio_medio": pytest.approx(201),
        }
    ]


def test_endpoint_cartera_calcula_valor_actual_y_diferencia():
    crear_operacion_cartera("compra", 5, 200, "2025-01-01", 5)

    response = TestClient(app).get(
        "/api/cartera",
        params={"usuario": "pruebas_regresion"},
    )

    assert response.status_code == 200
    posicion = response.json()["datos"][0]
    assert posicion["num_titulos"] == 5
    assert posicion["precio_actual"] == 250
    assert posicion["total_invertido"] == 1005
    assert posicion["total_actual"] == 1250
    assert posicion["diferencia"] == 245
    assert posicion["variacion_compra"] == pytest.approx(24.38)


def test_fifo_rechaza_venta_que_no_tiene_compra_previa():
    add_operacion(
        usuario="pruebas_regresion",
        tipo="venta",
        ticker="ANA.MC",
        fecha="2025-01-01",
        titulos=1,
        precio=10,
        comision=0,
        moneda="EUR",
    )

    with pytest.raises(ValueError, match="No hay títulos disponibles"):
        calcular_posiciones_abiertas("pruebas_regresion")
