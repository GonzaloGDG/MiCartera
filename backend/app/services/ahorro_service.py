"""
Lógica de negocio del ahorro.
"""

from app.repositories.ahorro_repository import (
    get_movimientos_usuario,
    add_movimiento,
    eliminar_movimiento,
)

from app.repositories.liquidez_repository import (
    get_liquidez_usuario,
    modificar_liquidez,
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

def obtener_liquidez(usuario: str):
    # 2. Obtener liquidez actual
    cuentas = get_liquidez_usuario(usuario)

    # De momento trabajamos con EUR
    cuenta_eur = next(
        (
            cuenta
            for cuenta in cuentas
            if cuenta["moneda"] == "EUR"
        ),
        None
    )

    if cuenta_eur is None:
        raise ValueError(
            f"No se encontró cuenta EUR para {usuario}"
        )

    return cuenta_eur["importe"]

def calcular_nueva_liquidez (usuario: str, tipo: str, importe: float):
    liquidez_actual = obtener_liquidez(usuario)

    if tipo == "ingreso":
        nueva_liquidez = (
            liquidez_actual + importe
        )

    elif tipo == "retirada":
        nueva_liquidez = (
            liquidez_actual - importe
        )

    else:
        raise ValueError(
            f"Tipo de movimiento no válido: {tipo}"
        )

    # 4. Guardar nueva liquidez
    modificar_liquidez(
        usuario=usuario,
        importe=nueva_liquidez,
        moneda="EUR",
    )

def crear_movimiento_ahorro(
    usuario: str,
    tipo: str,
    importe: float,
    fecha: str
):

    # 1. Guardar movimiento
    movimiento = add_movimiento(
        usuario=usuario,
        tipo=tipo,
        importe=importe,
        fecha=fecha,
    )

    # 2. Actualizar liquidez
    nueva_liquidez = calcular_nueva_liquidez(
        usuario=usuario,
        tipo=tipo,
        importe=importe,
    )

    return {
        "movimiento": movimiento,
        "liquidez": nueva_liquidez,
    }
    
def borrar_movimiento_ahorro(
    usuario: str,
    movimiento_id: int
):

    # 1. Buscar el movimiento antes de eliminarlo
    movimientos = get_movimientos_usuario(usuario)

    movimiento = next(
        (
            movimiento
            for movimiento in movimientos
            if movimiento["id"] == movimiento_id
        ),
        None
    )

    if movimiento is None:
        raise ValueError(
            f"No se encontró el movimiento {movimiento_id}"
        )

    # 2. Obtener los datos del movimiento
    tipo = movimiento["tipo"]
    importe = movimiento["importe"]

    # 3. Obtener la liquidez actual
    liquidez_actual = obtener_liquidez(usuario)

    # 4. Revertir el efecto sobre la liquidez
    if tipo == "ingreso":

        # Si eliminamos un ingreso,
        # quitamos ese importe de la liquidez
        nueva_liquidez = (
            liquidez_actual - importe
        )

    elif tipo == "retirada":

        # Si eliminamos una retirada,
        # devolvemos ese importe a la liquidez
        nueva_liquidez = (
            liquidez_actual + importe
        )

    else:
        raise ValueError(
            f"Tipo de movimiento no válido: {tipo}"
        )

    # 5. Actualizar liquidez
    modificar_liquidez(
        usuario=usuario,
        importe=nueva_liquidez,
        moneda="EUR"
    )

    # 6. Eliminar movimiento
    movimiento_eliminado = eliminar_movimiento(
        usuario=usuario,
        movimiento_id=movimiento_id
    )

    return movimiento_eliminado

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