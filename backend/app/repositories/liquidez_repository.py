"""
Repositorio de acceso a liquidez.

Actualmente lee los datos desde liquidez.json.
En el futuro leerá desde PostgreSQL.
"""

from app.repositories.base_repository import (
    load_json,
    save_json,
)

FILENAME = "liquidez.json"

def get_liquidez_usuario(usuario: str):

    liquidez = load_json(FILENAME)

    return [
        cuenta
        for cuenta in liquidez
        if cuenta["usuario"] == usuario
    ]

def modificar_liquidez(usuario: str, importe: float, moneda: str):

    liquidez = load_json(FILENAME)

    for cuenta in liquidez:

        if (
            cuenta["usuario"] == usuario
            and cuenta["moneda"] == moneda
        ):

            cuenta["importe"] = float(importe)

            save_json(
                FILENAME,
                liquidez
            )

            return cuenta

    liquidez.append({
        "usuario": usuario,
        "moneda": moneda,
        "importe": float(importe),
    })

    save_json(
        FILENAME,
        liquidez,
    )

    return liquidez[-1]