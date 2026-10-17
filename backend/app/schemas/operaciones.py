"""Schemas relacionados con operaciones de compra, venta y dividendo."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class OperacionCreateRequest(BaseModel):
    usuario: str
    tipo: Literal["compra", "venta", "dividendo"]
    ticker: str
    fecha: str = Field(
        default_factory=lambda: date.today().isoformat()
    )
    titulos: float
    precio: float
    comision: float
    moneda: str = "EUR"
    confirmar_precio_cero: bool = False


class OperacionResponse(BaseModel):
    ok: bool
    mensaje: str