"""
Lógica de negocio de la liquidez.
"""

from app.repositories.liquidez_repository import (
    get_liquidez_usuario,
)


def obtener_liquidez(usuario: str):

    cuentas = get_liquidez_usuario(usuario)

    total = sum(
        cuenta["importe"]
        for cuenta in cuentas
        if cuenta["moneda"] == "EUR"
    )

    return {
        "ok": True,
        "datos": cuentas,
        "total": total,
        "moneda": "EUR",
    }