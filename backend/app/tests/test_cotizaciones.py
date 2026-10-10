from fastapi.testclient import TestClient

from app.main import app
from app.providers import yahoo_finance
from app.routes import cotizaciones as cotizaciones_route


def test_endpoint_cotizacion_reenvia_datos_del_servicio(monkeypatch):
    expected = {
        "ok": True,
        "datos": {
            "ticker": "ANA.MC",
            "nombre": "Acciona",
            "precio_actual": 250,
            "variacion": 5,
            "variacion_pct": 2,
            "moneda": "EUR",
            "mercado": "MCE",
            "sector": "Industrials",
        },
    }
    monkeypatch.setattr(
        cotizaciones_route,
        "obtener_cotizacion",
        lambda ticker: expected,
    )

    response = TestClient(app).get("/api/cotizacion/ANA.MC")

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["datos"]["ticker"] == "ANA.MC"
    assert response.json()["datos"]["precio_actual"] == 250
    assert response.json()["datos"]["variacion_pct"] == 2


def test_endpoint_historico_reenvia_parametros_y_resultados(monkeypatch):
    expected = {"ok": True, "ticker": "ANA.MC", "datos": []}
    calls = []

    def fake_historico(ticker, periodo, intervalo):
        calls.append((ticker, periodo, intervalo))
        return expected

    monkeypatch.setattr(
        cotizaciones_route,
        "obtener_historico",
        fake_historico,
    )
    response = TestClient(app).get(
        "/api/historico/ANA.MC",
        params={"periodo": "6mo", "intervalo": "1wk"},
    )

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["ticker"] == "ANA.MC"
    assert response.json()["datos"] == []
    assert calls == [("ANA.MC", "6mo", "1wk")]


def test_proveedor_mapea_datos_de_yahoo_sin_llamada_externa(monkeypatch):
    class FakeYahooTicker:
        info = {
            "currentPrice": 42.5,
            "previousClose": 40,
            "regularMarketChangePercent": 6.25,
            "currency": "EUR",
        }

    monkeypatch.setattr(yahoo_finance.yf, "Ticker", lambda ticker: FakeYahooTicker())

    resultado = yahoo_finance.get_cotizacion("ana.mc")

    assert resultado["ok"] is True
    assert resultado["datos"]["ticker"] == "ANA.MC"
    assert resultado["datos"]["precio_actual"] == 42.5
    assert resultado["datos"]["variacion"] == 2.5
    assert resultado["datos"]["moneda"] == "EUR"


def test_proveedor_formatea_historico_y_trata_periodo_sin_datos(monkeypatch):
    class FakeDate:
        def strftime(self, formato):
            return "2026-10-01 00:00"

    class FakeHistory:
        empty = False

        def iterrows(self):
            return [
                (
                    FakeDate(),
                    {
                        "Open": 10.12345,
                        "High": 12.34567,
                        "Low": 9.98765,
                        "Close": 11.23456,
                        "Volume": 123,
                    },
                )
            ]

    class FakeYahooTicker:
        def history(self, period, interval):
            assert (period, interval) == ("3mo", "1wk")
            return FakeHistory()

    monkeypatch.setattr(yahoo_finance.yf, "Ticker", lambda ticker: FakeYahooTicker())

    resultado = yahoo_finance.get_historico("ana.mc", "3mo", "1wk")

    assert resultado == {
        "ok": True,
        "ticker": "ANA.MC",
        "datos": [
            {
                "fecha": "2026-10-01 00:00",
                "open": 10.1235,
                "high": 12.3457,
                "low": 9.9877,
                "close": 11.2346,
                "volumen": 123,
            }
        ],
    }

    class EmptyHistory:
        empty = True

    monkeypatch.setattr(
        FakeYahooTicker,
        "history",
        lambda self, period, interval: EmptyHistory(),
    )
    resultado_vacio = yahoo_finance.get_historico("ana.mc")
    assert resultado_vacio == {
        "ok": False,
        "mensaje": "No se encontraron datos históricos",
    }
