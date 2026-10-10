from fastapi.testclient import TestClient

from app.main import app
from app.tasks import ticker_updater


def test_endpoint_tickers_devuelve_catalogo_ordenado_por_nombre():
    response = TestClient(app).get("/api/tickers")

    assert response.status_code == 200
    assert [
        ticker["nombre"]
        for ticker in response.json()["datos"]
    ] == ["Acciona", "Acerinox"]


def test_actualizador_guarda_cotizaciones_y_cuenta_fallos(monkeypatch):
    respuestas = {
        "ANA.MC": {
            "ok": True,
            "datos": {
                "precio_actual": 251,
                "variacion": 1,
                "variacion_pct": 0.4,
                "precio_cierre": 250,
                "moneda": "EUR",
                "mercado": "MCE",
                "sector": "Industrials",
                "max_52s": 300,
                "min_52s": 200,
                "capitalizacion": 1000,
                "volumen": 100,
            },
        },
        "ACX.MC": {"ok": False, "mensaje": "sin cotización"},
    }
    monkeypatch.setattr(
        ticker_updater,
        "get_cotizacion",
        lambda ticker: respuestas[ticker],
    )
    monkeypatch.setattr(ticker_updater, "sleep", lambda seconds: None)

    resultado = ticker_updater.actualizar_precios()
    tickers = ticker_updater.load_tickers()

    assert resultado["ok"] is False
    assert resultado["actualizados"] == 1
    assert resultado["errores"] == 1
    assert tickers[0]["precio_actual"] == 251
    assert tickers[0]["ultimo_update"] == resultado["ultimo_update"]
    assert tickers[1]["precio_actual"] == 12.5
    assert tickers[1]["ultimo_update"] == "2026-10-02 10:00:00"
