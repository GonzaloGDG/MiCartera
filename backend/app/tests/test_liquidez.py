import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.liquidez_service import (
    establecer_liquidez,
    obtener_importe_liquidez,
    obtener_liquidez,
)


def test_consultar_liquidez_devuelve_solo_total_eur():
    assert obtener_liquidez("pruebas_regresion") == {
        "ok": True,
        "datos": [
            {
                "usuario": "pruebas_regresion",
                "moneda": "EUR",
                "importe": 10000.0,
            }
        ],
        "total": 10000.0,
        "moneda": "EUR",
    }


def test_endpoint_consulta_liquidez_devuelve_total_eur():
    response = TestClient(app).get("/api/liquidez?usuario=pruebas_regresion")

    assert response.status_code == 200
    assert response.json() == {
        "ok": True,
        "datos": [
            {
                "usuario": "pruebas_regresion",
                "moneda": "EUR",
                "importe": 10000.0,
            }
        ],
        "total": 10000.0,
        "moneda": "EUR",
    }


def test_endpoint_actualiza_liquidez_y_crea_cuenta_si_no_existe():
    response = TestClient(app).put(
        "/api/liquidez",
        json={
            "usuario": "usuario_nuevo",
            "moneda": "EUR",
            "importe": 750.0,
        },
    )

    assert response.status_code == 200
    assert response.json()["importe"] == 750.0
    assert obtener_importe_liquidez("usuario_nuevo") == 750.0


def test_liquidez_no_puede_ser_negativa():
    with pytest.raises(ValueError, match="no puede ser negativa"):
        establecer_liquidez("pruebas_regresion", -1)

    assert obtener_importe_liquidez("pruebas_regresion") == 10000.0


def test_endpoint_devuelve_400_si_la_liquidez_es_negativa():
    response = TestClient(app).put(
        "/api/liquidez",
        json={
            "usuario": "pruebas_regresion",
            "moneda": "EUR",
            "importe": -1,
        },
    )

    assert response.status_code == 400
    assert "no puede ser negativa" in response.json()["detail"]
    assert obtener_importe_liquidez("pruebas_regresion") == 10000
