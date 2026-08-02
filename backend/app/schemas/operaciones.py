"""
Schemas relacionados con operaciones de compra y venta.
"""

from pydantic import BaseModel
from typing import Literal


class OperacionCreateRequest(BaseModel):
    usuario: str
    tipo: Literal["compra", "venta"]
    ticker: str
    fecha: str
    titulos: float
    precio: float
    comision: float = 0.0
    moneda: str = "EUR"


class OperacionResponse(BaseModel):
    ok: bool
    mensaje: str