import json

import pytest

from app.repositories import auth_repository, base_repository
from app.services import cotizaciones_service
from app.tasks import ticker_updater


@pytest.fixture(autouse=True)
def isolated_json_data(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    data = {
        "usuarios.json": [
            {
                "id": 1,
                "username": "pruebas_regresion",
                "password": "clave",
                "nombre": "Usuario de pruebas",
                "rol": "user",
            }
        ],
        "liquidez.json": [
            {
                "usuario": "pruebas_regresion",
                "moneda": "EUR",
                "importe": 10000.0,
            }
        ],
        "operaciones.json": [],
        "movimientos_ahorro.json": [],
        "tickers.json": [
            {
                "ticker": "ANA.MC",
                "nombre": "Acciona",
                "ultimo_update": "2026-10-01 10:00:00",
                "precio_actual": 250.0,
                "variacion_pct": 2.0,
                "moneda": "EUR",
            },
            {
                "ticker": "ACX.MC",
                "nombre": "Acerinox",
                "ultimo_update": "2026-10-02 10:00:00",
                "precio_actual": 12.5,
                "variacion_pct": -1.0,
                "moneda": "EUR",
            },
        ],
    }

    for filename, contents in data.items():
        (data_dir / filename).write_text(
            json.dumps(contents),
            encoding="utf-8",
        )

    monkeypatch.setattr(base_repository, "DATA_DIR", data_dir)
    monkeypatch.setattr(
        auth_repository,
        "USUARIOS_FILE",
        data_dir / "usuarios.json",
    )
    monkeypatch.setattr(
        cotizaciones_service,
        "TICKERS_FILE",
        data_dir / "tickers.json",
    )
    monkeypatch.setattr(
        ticker_updater,
        "TICKERS_FILE",
        str(data_dir / "tickers.json"),
    )
