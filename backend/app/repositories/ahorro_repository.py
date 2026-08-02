"""
Repositorio de acceso a movimientos de ahorro.

Actualmente lee y escribe los datos desde movimientos_ahorro.json.
En el futuro leerá desde PostgreSQL.
"""

from app.repositories.base_repository import (
    load_json,
    save_json,
    next_id,
)

FILENAME = "movimientos_ahorro.json"

def get_movimientos_usuario(usuario: str):

    movimientos = load_json(
        FILENAME
    )

    return [
        movimiento
        for movimiento in movimientos
        if movimiento["usuario"] == usuario
    ]


def add_movimiento(
    usuario: str,
    tipo: str,
    importe: float,
    fecha: str
):

    movimientos = load_json(
        "movimientos_ahorro.json"
    )

    # Generar nuevo ID
    if movimientos:
        nuevo_id = next_id(movimientos)
    else:
        nuevo_id = 1


    nuevo_movimiento = {

        "id": nuevo_id,

        "usuario": usuario,

        "tipo": tipo,

        "importe": float(importe),

        "fecha": fecha

    }


    movimientos.append(
        nuevo_movimiento
    )


    save_json(
        FILENAME,
        movimientos
    )


    return nuevo_movimiento

def eliminar_movimiento(usuario: str, movimiento_id: int):

    movimientos = load_json(
        FILENAME
    )

    movimiento_encontrado = None

    for movimiento in movimientos:

        if (
            movimiento["usuario"] == usuario
            and movimiento["id"] == movimiento_id
        ):
            movimiento_encontrado = movimiento
            break

    if movimiento_encontrado is None:
        raise ValueError(
            f"No se encontró el movimiento {movimiento_id}"
        )

    movimientos.remove(
        movimiento_encontrado
    )

    save_json(
        FILENAME,
        movimientos
    )

    return movimiento_encontrado