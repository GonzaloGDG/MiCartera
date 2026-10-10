"""
Lógica de negocio del ahorro.
"""

from app.repositories.ahorro_repository import (
    get_movimientos_usuario,
    add_movimiento,
    eliminar_movimiento,
    delete_all_movimientos,
)

from app.services.liquidez_service import (
    obtener_importe_liquidez,
    establecer_liquidez,
)

from app.services.cotizaciones_service import (
    obtener_ultima_actualizacion,
)

def obtener_ahorro(usuario: str):

    movimientos = get_movimientos_usuario(usuario)

    # Ordenar movimientos del más reciente al más antiguo
    movimientos = sorted(
        movimientos,
        key=lambda movimiento: movimiento["fecha"],
        reverse=True,
    )

    # Total neto histórico
    total_neto = 0

    # Totales por año
    totales_anuales = {}

    ultima_actualizacion = obtener_ultima_actualizacion()

    for movimiento in movimientos:

        importe = movimiento["importe"]
        tipo = movimiento["tipo"]
        fecha = movimiento["fecha"]

        # Ingresos suman
        if tipo == "ingreso":
            importe_neto = importe

        # Retiradas restan
        elif tipo == "retirada":
            importe_neto = -importe

        else:
            continue

        total_neto += importe_neto

        # Obtener año
        año = fecha[:4]

        if año not in totales_anuales:
            totales_anuales[año] = 0

        totales_anuales[año] += importe_neto

    return {
        "ok": True,
        "datos": movimientos,
        "total_neto": round(total_neto, 2),
        "totales_anuales": totales_anuales,
        "ultima_actualizacion": ultima_actualizacion,
    }


def actualizar_liquidez_movimiento (usuario: str, tipo: str, importe: float):
    
    liquidez_actual = obtener_importe_liquidez(usuario)

    if tipo == "ingreso":
        nueva_liquidez = liquidez_actual + importe

    elif tipo == "retirada":
        if importe > liquidez_actual:
            raise ValueError(
                "La retirada supera la liquidez disponible"
            )
        nueva_liquidez = liquidez_actual - importe

    else:
        raise ValueError(
            f"Tipo de movimiento no válido: {tipo}"
        )

    establecer_liquidez(
        usuario=usuario,
        importe=nueva_liquidez,
)   

def crear_movimiento_ahorro(
    usuario: str,
    tipo: str,
    importe: float,
    fecha: str
):

    if tipo not in {"ingreso", "retirada"}:
        raise ValueError(
            f"Tipo de movimiento no válido: {tipo}"
        )

    if importe <= 0:
        raise ValueError(
            "El importe debe ser mayor que cero"
        )

    liquidez_actual = obtener_importe_liquidez(usuario)
    if tipo == "retirada" and importe > liquidez_actual:
        raise ValueError(
            "La retirada supera la liquidez disponible"
        )

    movimiento = add_movimiento(
        usuario=usuario,
        tipo=tipo,
        importe=importe,
        fecha=fecha,
    )

    # 2. Actualizar liquidez
    nueva_liquidez = (
        liquidez_actual + importe
        if tipo == "ingreso"
        else liquidez_actual - importe
    )
    establecer_liquidez(
        usuario=usuario,
        importe=nueva_liquidez,
    )

    return {
        "movimiento": movimiento,
        "liquidez": nueva_liquidez,
    }
    
def borrar_movimiento_ahorro(
    usuario: str,
    movimiento_id: int,
):

    movimientos = get_movimientos_usuario(usuario)

    movimiento = next(
        (
            movimiento
            for movimiento in movimientos
            if movimiento["id"] == movimiento_id
        ),
        None,
    )

    if movimiento is None:
        raise ValueError(
            f"No se encontró el movimiento {movimiento_id}"
        )

    # Obtener los datos del movimiento
    tipo = movimiento["tipo"]
    importe = movimiento["importe"]

    if tipo == "ingreso":
        tipo_inverso = "retirada"
    elif tipo == "retirada":
        tipo_inverso = "ingreso"
    else:
        raise ValueError(
            f"Tipo de movimiento no válido: {tipo}"
    )

    actualizar_liquidez_movimiento(
        usuario=usuario,
        tipo=tipo_inverso,
        importe=importe,
    )

    movimiento_eliminado = eliminar_movimiento(
        usuario=usuario,
        movimiento_id=movimiento_id,
    )

    return movimiento_eliminado

""" 
    Borrado de todos los movimientos de un usuario, 
    uso principal en las pruebas de rgresión
"""
def borrar_todos_movimientos(usuario: str):

    delete_all_movimientos(usuario)