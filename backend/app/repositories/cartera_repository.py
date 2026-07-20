"""
Repositorio de acceso a cartera.

Actualmente lee los datos desde cartera.json.
En el futuro leerá desde PostgreSQL sin cambiar
el resto de la aplicación.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def _load_json(filename: str):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as file:
        return json.load(file)

def get_cartera_usuario(usuario: str):
    cartera = _load_json("cartera.json")

    return [
        posicion
        for posicion in cartera
        if posicion["usuario"] == usuario
    ]

def get_tickers():
    tickers = _load_json("tickers.json")

    return {
        ticker["ticker"]: ticker
        for ticker in tickers
    }