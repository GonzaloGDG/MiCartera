"""
Repositorio de operaciones.

Actualmente lee y escribe los datos desde operaciones.json.
En el futuro leerá desde PostgreSQL.
"""

from app.repositories.base_repository import (
    load_json,
    save_json,
    next_id,
)

FILENAME = "operaciones.json"

def add_operacion(
    usuario: str,
    tipo: str,
    ticker: str,
    fecha: str,
    titulos: float,
    precio: float,
    comision: float,
    moneda: str,
):

    operaciones = load_json(
        FILENAME
    )

    # Generar nuevo ID
    if operaciones:
        nuevo_id = next_id(operaciones)
    else:
        nuevo_id = 1


    nueva_operacion = {
        "id": nuevo_id,
        "usuario": usuario,
        "tipo": tipo,
        "ticker": ticker,
        "fecha": fecha,
        "titulos": titulos,
        "precio": precio,
        "comision": comision,
        "moneda": moneda,
    }

    operaciones.append(nueva_operacion)

    save_json(FILENAME, operaciones)

    return nueva_operacion


def get_operacion(
    usuario: str,
    operacion_id: int,
):

    operaciones = load_json(FILENAME)

    return next(
        (
            operacion
            for operacion in operaciones
            if operacion["id"] == operacion_id
            and operacion["usuario"] == usuario
        ),
        None,
    )

def obtener_operaciones(usuario: str):

    operaciones = load_json(FILENAME)

    return [
        operacion
        for operacion in operaciones
        if operacion["usuario"] == usuario
    ]

def delete_operacion(
    usuario: str,
    operacion_id: int,
):

    operaciones = load_json(FILENAME)

    operacion = next(
        (
            op
            for op in operaciones
            if op["usuario"] == usuario
            and op["id"] == operacion_id
        ),
        None,
    )

    if operacion is None:
        raise ValueError(
            f"No existe la operación {operacion_id}"
        )

    operaciones = [
        op
        for op in operaciones
        if not (
            op["usuario"] == usuario
            and op["id"] == operacion_id
        )
    ]

    save_json(
        FILENAME,
        operaciones,
    )

    return operacion

""" 
    Borrado de todas las operaciones de un usuario, 
    uso principal en las pruebas de rgresión
"""
def delete_all_operaciones(usuario: str):

    operaciones = load_json(FILENAME)

    operaciones = [
        operacion
        for operacion in operaciones
        if operacion["usuario"] != usuario
    ]

    save_json(
        FILENAME,
        operaciones,
    )