"""
Lógica de negocio de la liquidez.
"""

from app.repositories.liquidez_repository import (
    get_liquidez_usuario,
    modificar_liquidez,
    delete_all_operaciones,
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


def obtener_importe_liquidez(usuario: str):

    cuentas = get_liquidez_usuario(usuario)

    cuenta_eur = next(
        (
            cuenta
            for cuenta in cuentas
            if cuenta["moneda"] == "EUR"
        ),
        None,
    )

    if cuenta_eur is None:
        raise ValueError(
            f"No se encontró cuenta EUR para {usuario}"
        )

    return cuenta_eur["importe"]

def establecer_liquidez(
    usuario: str,
    importe: float,
    moneda: str = "EUR",
):
    if importe < 0:
        raise ValueError(
            "La liquidez no puede ser negativa"
        )

    modificar_liquidez(
        usuario=usuario,
        importe=importe,
        moneda=moneda,
    )

    return {
        "ok": True,
        "mensaje": "Liquidez actualizada correctamente",
        "importe": importe,
        "moneda": moneda,
    }

    