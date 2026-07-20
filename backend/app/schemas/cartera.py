from pydantic import BaseModel


class Posicion(BaseModel):
    ticker: str
    nombre: str
    num_titulos: int
    precio_compra: float
    precio_actual: float
    variacion_hoy: float
    variacion_compra: float
    total_invertido: float
    total_actual: float
    diferencia: float
    moneda: str


class CarteraResponse(BaseModel):
    ok: bool
    datos: list[Posicion]