from fastapi.testclient import TestClient

from app.main import app


def test_login_acepta_credenciales_validas_y_espacios_exteriores():
    response = TestClient(app).post(
        "/api/login",
        json={"username": " pruebas_regresion ", "password": " clave "},
    )

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["username"] == "pruebas_regresion"
    assert response.json()["nombre"] == "Usuario de pruebas"
    assert response.json()["rol"] == "user"


def test_login_rechaza_credenciales_incorrectas():
    response = TestClient(app).post(
        "/api/login",
        json={"username": "pruebas_regresion", "password": "incorrecta"},
    )

    assert response.status_code == 200
    assert response.json()["ok"] is False
    assert response.json()["mensaje"] == "Usuario o contraseña incorrectos"
