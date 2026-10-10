import json

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories import base_repository
from app.schemas.operaciones import OperacionCreateRequest
from app.services.liquidez_service import obtener_importe_liquidez
from app.services.operaciones_service import (
    borrar_operacion,
    crear_operacion,
    get_operaciones_usuario,
    obtener_titulos_disponibles,
)


def crear_datos_operacion(tipo, titulos, precio, comision=0, ticker="ANA.MC"):
    return OperacionCreateRequest(
        usuario="pruebas_regresion",
        tipo=tipo,
        ticker=ticker,
        fecha="2025-01-01",
        titulos=titulos,
        precio=precio,
        comision=comision,
    )


def test_compra_venta_y_borrado_revierten_titulos_y_liquidez():
    compra = crear_operacion(crear_datos_operacion("compra", 10, 100, 5))
    venta = crear_operacion(crear_datos_operacion("venta", 4, 120, 2))

    assert obtener_importe_liquidez("pruebas_regresion") == 9473
    assert obtener_titulos_disponibles("pruebas_regresion", "ANA.MC") == 6

    venta_borrada = borrar_operacion("pruebas_regresion", venta["id"])
    assert venta_borrada["id"] == venta["id"]
    assert obtener_importe_liquidez("pruebas_regresion") == 8995
    assert obtener_titulos_disponibles("pruebas_regresion", "ANA.MC") == 10

    borrar_operacion("pruebas_regresion", compra["id"])
    assert obtener_importe_liquidez("pruebas_regresion") == 10000
    assert get_operaciones_usuario("pruebas_regresion")["datos"] == []


def test_api_rechaza_venta_de_titulos_no_disponibles():
    response = TestClient(app).post(
        "/api/operaciones",
        json={
            "usuario": "pruebas_regresion",
            "tipo": "venta",
            "ticker": "ANA.MC",
            "fecha": "2025-01-01",
            "titulos": 1,
            "precio": 100,
            "comision": 0,
            "moneda": "EUR",
        },
    )

    assert response.status_code == 400
    assert "suficientes títulos" in response.json()["detail"]


@pytest.mark.parametrize(
    "operacion",
    [
        crear_datos_operacion("compra", 0, 100),
        crear_datos_operacion("compra", 1, 0),
        crear_datos_operacion("compra", 1, 100, -1),
        crear_datos_operacion("compra", 1, 100, ticker="INVALIDO"),
        crear_datos_operacion("compra", 101, 100),
    ],
)
def test_operacion_invalida_no_se_persiste(operacion):
    with pytest.raises(ValueError):
        crear_operacion(operacion)

    operaciones = json.loads(
        (base_repository.DATA_DIR / "operaciones.json").read_text(
            encoding="utf-8"
        )
    )
    assert operaciones == []
    assert obtener_importe_liquidez("pruebas_regresion") == 10000


def test_no_se_puede_borrar_operacion_que_no_sea_la_ultima_del_ticker():
    primera = crear_operacion(crear_datos_operacion("compra", 5, 10))
    crear_operacion(crear_datos_operacion("compra", 2, 20))
    saldo_antes = obtener_importe_liquidez("pruebas_regresion")

    with pytest.raises(ValueError, match="última operación"):
        borrar_operacion("pruebas_regresion", primera["id"])

    assert obtener_importe_liquidez("pruebas_regresion") == saldo_antes
    assert len(get_operaciones_usuario("pruebas_regresion")["datos"]) == 2


def test_operaciones_se_listan_en_orden_de_fecha_descendente():
    crear_operacion(crear_datos_operacion("compra", 1, 10))
    segunda = crear_operacion(
        OperacionCreateRequest(
            usuario="pruebas_regresion",
            tipo="compra",
            ticker="ACX.MC",
            fecha="2025-02-01",
            titulos=1,
            precio=10,
        )
    )

    lista = get_operaciones_usuario("pruebas_regresion")["datos"]
    assert lista[0]["id"] == segunda["id"]
