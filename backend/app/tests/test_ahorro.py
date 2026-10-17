import json
from datetime import date

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories import base_repository
from app.services.ahorro_service import (
    borrar_movimiento_ahorro,
    crear_movimiento_ahorro,
    obtener_ahorro,
)
from app.services.liquidez_service import obtener_importe_liquidez


def test_movimientos_ahorro_actualizan_liquidez_y_pueden_borrarse():
    ingreso = crear_movimiento_ahorro(
        "pruebas_regresion",
        "ingreso",
        500,
        "2025-01-01",
    )
    retirada = crear_movimiento_ahorro(
        "pruebas_regresion",
        "retirada",
        125,
        "2025-02-01",
    )

    assert ingreso["liquidez"] == 10500
    assert retirada["liquidez"] == 10375
    assert obtener_importe_liquidez("pruebas_regresion") == 10375

    eliminado = borrar_movimiento_ahorro(
        "pruebas_regresion",
        retirada["movimiento"]["id"],
    )

    assert eliminado["tipo"] == "retirada"
    assert obtener_importe_liquidez("pruebas_regresion") == 10500
    assert obtener_ahorro("pruebas_regresion")["total_neto"] == 500


def test_endpoint_ahorro_devuelve_liquidez_y_resumen_anual():
    año_actual = date.today().year
    response = TestClient(app).post(
        "/api/ahorro",
        json={
            "usuario": "pruebas_regresion",
            "tipo": "ingreso",
            "importe": 300,
            "fecha": f"{año_actual}-06-15",
        },
    )

    assert response.status_code == 200
    assert response.json()["liquidez"] == 10300

    resumen = TestClient(app).get(
        "/api/ahorro",
        params={"usuario": "pruebas_regresion"},
    )
    assert resumen.status_code == 200
    assert resumen.json()["total_neto"] == 300
    assert resumen.json()["totales_anuales"] == {
        str(año): (300 if año == año_actual else 0)
        for año in range(año_actual - 4, año_actual + 1)
    }
    assert resumen.json()["liquidez"] == 10300


def test_resumen_incluye_cuatro_años_y_base_anterior_con_variaciones_netas(
    monkeypatch,
):
    class FechaFija(date):
        @classmethod
        def today(cls):
            return cls(2026, 10, 17)

    monkeypatch.setattr("app.services.ahorro_service.date", FechaFija)
    año_actual = FechaFija.today().year

    crear_movimiento_ahorro(
        "pruebas_regresion", "ingreso", 1200, f"{año_actual - 3}-01-01"
    )
    crear_movimiento_ahorro(
        "pruebas_regresion", "retirada", 200, f"{año_actual - 3}-02-01"
    )
    crear_movimiento_ahorro(
        "pruebas_regresion", "ingreso", 1000, f"{año_actual - 1}-01-01"
    )
    crear_movimiento_ahorro(
        "pruebas_regresion", "ingreso", 1500, f"{año_actual}-01-01"
    )

    resumen = obtener_ahorro("pruebas_regresion")

    assert resumen["total_neto"] == 3500
    assert resumen["totales_anuales"] == {
        str(año_actual - 4): 0,
        str(año_actual - 3): 1000,
        str(año_actual - 2): 0,
        str(año_actual - 1): 1000,
        str(año_actual): 1500,
    }


@pytest.mark.parametrize(
    ("tipo", "importe"),
    [("desconocido", 10), ("ingreso", 0), ("ingreso", -10), ("retirada", 10001)],
)
def test_movimiento_invalido_no_modifica_datos(tipo, importe):
    with pytest.raises(ValueError):
        crear_movimiento_ahorro(
            "pruebas_regresion",
            tipo,
            importe,
            "2025-01-01",
        )

    movimientos = json.loads(
        (base_repository.DATA_DIR / "movimientos_ahorro.json").read_text(
            encoding="utf-8"
        )
    )
    assert movimientos == []
    assert obtener_importe_liquidez("pruebas_regresion") == 10000


def test_borrar_movimiento_inexistente_informa_el_error():
    with pytest.raises(ValueError, match="No se encontró"):
        borrar_movimiento_ahorro("pruebas_regresion", 999)


def test_endpoint_devuelve_400_si_se_rechaza_un_movimiento():
    response = TestClient(app).post(
        "/api/ahorro",
        json={
            "usuario": "pruebas_regresion",
            "tipo": "retirada",
            "importe": 10001,
            "fecha": "2025-01-01",
        },
    )

    assert response.status_code == 400
    assert "supera la liquidez" in response.json()["detail"]
    assert obtener_importe_liquidez("pruebas_regresion") == 10000


def test_endpoint_devuelve_400_al_borrar_movimiento_inexistente():
    response = TestClient(app).delete(
        "/api/ahorro/999",
        params={"usuario": "pruebas_regresion"},
    )

    assert response.status_code == 400
    assert "No se encontró" in response.json()["detail"]
