from pydantic import BaseModel


class Cotizacion(BaseModel):
    ticker: str
    nombre: str
    precio_actual: float
    precio_apertura: float | None = None
    precio_cierre: float | None = None
    variacion: float
    variacion_pct: float
    moneda: str
    mercado: str
    sector: str
    max_52s: float | None = None
    min_52s: float | None = None
    capitalizacion: int | None = None
    volumen: int | None = None


class CotizacionResponse(BaseModel):
    ok: bool
    datos: Cotizacion | None = None
    mensaje: str | None = None


class RegistroHistorico(BaseModel):
    fecha: str
    open: float
    high: float
    low: float
    close: float
    volumen: int


class HistoricoResponse(BaseModel):
    ok: bool
    ticker: str | None = None
    datos: list[RegistroHistorico] = []
    mensaje: str | None = None