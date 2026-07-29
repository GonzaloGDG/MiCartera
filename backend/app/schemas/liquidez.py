"""
Schemas de la liquidez.
"""

from pydantic import BaseModel


class CuentaLiquidez(BaseModel):
    usuario: str
    moneda: str
    importe: float


class LiquidezResponse(BaseModel):
    ok: bool
    datos: list[CuentaLiquidez]
    total: float
    moneda: str

class ModificarLiquidezRequest(BaseModel):
    usuario: str
    moneda: str
    importe: float