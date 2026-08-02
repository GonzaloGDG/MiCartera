"""

Actualmente lee y escribe los datos desde fichero.json.
En el futuro leerá desde PostgreSQL.
"""

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_json(filename: str):

    with open(
        DATA_DIR / filename,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_json(filename: str, datos):

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

def next_id(datos):

    return (
        max(
            (
                elemento["id"]
                for elemento in datos
            ),
            default=0,
        )
        + 1
    )