"""
Schemas de ahorro y movimientos de la cuenta de valores.
"""

from pydantic import BaseModel


class MovimientoAhorro(BaseModel):
    id: int
    usuario: str
    tipo: str
    importe: float
    fecha: str


class AhorroResponse(BaseModel):
    ok: bool
    datos: list[MovimientoAhorro]
    total_neto: float
    totales_anuales: dict[str, float]