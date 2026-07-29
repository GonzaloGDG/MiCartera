"""
Repositorio de acceso a liquidez.

Actualmente lee los datos desde liquidez.json.
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

def get_liquidez_usuario(usuario: str):

    liquidez = _load_json("liquidez.json")

    return [
        cuenta
        for cuenta in liquidez
        if cuenta["usuario"] == usuario
    ]

def modificar_liquidez(usuario: str, importe: float, moneda: str):

    liquidez = _load_json("liquidez.json")

    for cuenta in liquidez: 

        if ( cuenta["usuario"] == usuario and cuenta["moneda"] == moneda ):

            cuenta["importe"] = float(importe)

            _save_json(
                "liquidez.json",
                liquidez
            )

            return cuenta

    raise ValueError(
        f"No se encontró cuenta de liquidez "
        f"para {usuario} en {moneda}"
    )