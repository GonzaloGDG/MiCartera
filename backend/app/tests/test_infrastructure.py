from fastapi.testclient import TestClient

from app.main import app


def test_api_raiz_informa_estado_correcto():
    response = TestClient(app).get("/")

    assert response.status_code == 200
    assert response.json() == {
        "application": "MiCartera",
        "framework": "FastAPI",
        "status": "OK",
    }
