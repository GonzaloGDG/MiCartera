import json

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
    response = TestClient(app).post(
        "/api/ahorro",
        json={
            "usuario": "pruebas_regresion",
            "tipo": "ingreso",
            "importe": 300,
            "fecha": "2024-06-15",
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
    assert resumen.json()["totales_anuales"] == {"2024": 300}
    assert resumen.json()["liquidez"] == 10300


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
