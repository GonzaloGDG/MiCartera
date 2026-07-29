"""
Repositorio de acceso a movimientos de ahorro.

Actualmente lee y escribe los datos desde movimientos_ahorro.json.
En el futuro leerá desde PostgreSQL.
"""

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def _load_json(filename: str):

    with open(
        DATA_DIR / filename,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def _save_json(filename: str, datos):

    with open(
        DATA_DIR / filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            datos,
            file,
            ensure_ascii=False,
            indent=2
        )


def get_movimientos_usuario(usuario: str):

    movimientos = _load_json(
        "movimientos_ahorro.json"
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

    movimientos = _load_json(
        "movimientos_ahorro.json"
    )

    # Generar nuevo ID
    if movimientos:

        nuevo_id = max(
            movimiento.get("id", 0)
            for movimiento in movimientos
        ) + 1

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


    _save_json(
        "movimientos_ahorro.json",
        movimientos
    )


    return nuevo_movimiento

def eliminar_movimiento(usuario: str, movimiento_id: int):

    movimientos = _load_json(
        "movimientos_ahorro.json"
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

    _save_json(
        "movimientos_ahorro.json",
        movimientos
    )

    return movimiento_encontrado