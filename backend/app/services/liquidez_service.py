"""
Lógica de negocio de la liquidez.
"""

from app.repositories.liquidez_repository import (
    get_liquidez_usuario,
    modificar_liquidez,
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


def obtener_importe_liquidez(
    usuario: str,
    moneda: str = "EUR",
    valor_por_defecto: float | None = None,
):

    cuentas = get_liquidez_usuario(usuario)

    cuenta_moneda = next(
        (
            cuenta
            for cuenta in cuentas
            if cuenta["moneda"] == moneda
        ),
        None,
    )

    if cuenta_moneda is None:
        if valor_por_defecto is not None:
            return valor_por_defecto
        raise ValueError(
            f"No se encontró cuenta {moneda} para {usuario}"
        )

    return cuenta_moneda["importe"]

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

    