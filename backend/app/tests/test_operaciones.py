import json

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories import base_repository
from app.schemas.operaciones import OperacionCreateRequest
from app.services.liquidez_service import obtener_importe_liquidez
from app.services.liquidez_service import establecer_liquidez
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


def test_api_crea_y_borra_operacion_revirtiendo_liquidez():
    cliente = TestClient(app)
    respuesta_creacion = cliente.post(
        "/api/operaciones",
        json={
            "usuario": "pruebas_regresion",
            "tipo": "compra",
            "ticker": "ANA.MC",
            "fecha": "2025-01-01",
            "titulos": 2,
            "precio": 100,
            "comision": 5,
            "moneda": "EUR",
        },
    )

    assert respuesta_creacion.status_code == 200
    operacion = respuesta_creacion.json()["datos"]
    assert obtener_importe_liquidez("pruebas_regresion") == 9795

    respuesta_borrado = cliente.delete(
        f"/api/operaciones/{operacion['id']}",
        params={"usuario": "pruebas_regresion"},
    )

    assert respuesta_borrado.status_code == 200
    assert respuesta_borrado.json()["datos"]["id"] == operacion["id"]
    assert obtener_importe_liquidez("pruebas_regresion") == 10000
    assert get_operaciones_usuario("pruebas_regresion")["datos"] == []


@pytest.mark.parametrize(
    "operacion",
    [
        crear_datos_operacion("compra", 0, 100),
        crear_datos_operacion("compra", 1, 100, -1),
        crear_datos_operacion("compra", 1, 100, ticker="INVALIDO"),
        crear_datos_operacion("compra", 101, 100),
        crear_datos_operacion("venta", 1, 0),
        crear_datos_operacion("dividendo", 1, 10),
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


def test_compra_con_precio_cero_se_registra_solo_tras_confirmacion():
    operacion_sin_confirmar = crear_datos_operacion("compra", 1, 0)
    with pytest.raises(ValueError, match="Confirme la compra"):
        crear_operacion(operacion_sin_confirmar)

    assert get_operaciones_usuario("pruebas_regresion")["datos"] == []
    assert obtener_importe_liquidez("pruebas_regresion") == 10000

    operacion_confirmada = crear_datos_operacion("compra", 1, 0)
    operacion_confirmada.confirmar_precio_cero = True
    operacion = crear_operacion(operacion_confirmada)

    assert operacion["precio"] == 0
    assert obtener_importe_liquidez("pruebas_regresion") == 10000


def test_dividendo_solo_admite_los_titulos_actuales_y_actualiza_liquidez():
    crear_operacion(crear_datos_operacion("compra", 10, 100))
    dividendo_invalido = crear_datos_operacion("dividendo", 9, 2)
    with pytest.raises(ValueError, match="deben coincidir"):
        crear_operacion(dividendo_invalido)

    dividendo = crear_operacion(
        crear_datos_operacion("dividendo", 10, 2, comision=1)
    )

    assert dividendo["tipo"] == "dividendo"
    assert obtener_importe_liquidez("pruebas_regresion") == 9019
    assert obtener_titulos_disponibles("pruebas_regresion", "ANA.MC") == 10

    borrar_operacion("pruebas_regresion", dividendo["id"])
    assert obtener_importe_liquidez("pruebas_regresion") == 9000


def test_operacion_actualiza_saldo_en_su_moneda_y_el_borrado_lo_revierte():
    establecer_liquidez(
        "pruebas_regresion",
        importe=20,
        moneda="USD",
    )
    compra = crear_datos_operacion("compra", 2, 10)
    compra.moneda = "USD"
    crear_operacion(compra)

    from app.services.liquidez_service import obtener_importe_liquidez

    assert obtener_importe_liquidez(
        "pruebas_regresion",
        moneda="USD",
    ) == 0

    venta = crear_datos_operacion("venta", 1, 15)
    venta.moneda = "USD"
    operacion_venta = crear_operacion(venta)
    assert obtener_importe_liquidez(
        "pruebas_regresion",
        moneda="USD",
    ) == 15

    borrar_operacion("pruebas_regresion", operacion_venta["id"])
    assert obtener_importe_liquidez(
        "pruebas_regresion",
        moneda="USD",
    ) == 0


def test_resumen_operaciones_incluye_seis_años_y_solo_compras_eur():
    from datetime import date

    año_actual = date.today().year
    crear_operacion(
        OperacionCreateRequest(
            usuario="pruebas_regresion",
            tipo="compra",
            ticker="ANA.MC",
            fecha=f"{año_actual - 1}-01-01",
            titulos=10,
            precio=100,
            comision=10,
        )
    )
    crear_operacion(
        OperacionCreateRequest(
            usuario="pruebas_regresion",
            tipo="compra",
            ticker="ACX.MC",
            fecha=f"{año_actual}-01-01",
            titulos=10,
            precio=150,
            comision=0,
        )
    )
    compra_usd = OperacionCreateRequest(
        usuario="pruebas_regresion",
        tipo="compra",
        ticker="ACX.MC",
        fecha=f"{año_actual}-02-01",
        titulos=1,
        precio=10,
        comision=0,
        moneda="USD",
    )
    establecer_liquidez(
        "pruebas_regresion",
        importe=20,
        moneda="USD",
    )
    crear_operacion(compra_usd)

    resumen = get_operaciones_usuario("pruebas_regresion")

    assert resumen["moneda_resumen"] == "EUR"
    assert resumen["total_invertido"] == 2510
    assert len(resumen["totales_anuales"]) == 6
    anual_por_año = {
        dato["año"]: dato
        for dato in resumen["totales_anuales"]
    }
    assert anual_por_año[año_actual]["total"] == 1500
    assert anual_por_año[año_actual]["variacion"] == 48.51


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
            comision=0,
        )
    )

    lista = get_operaciones_usuario("pruebas_regresion")["datos"]
    assert lista[0]["id"] == segunda["id"]
