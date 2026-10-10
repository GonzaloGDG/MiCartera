"""
Lógica de negocio de operaciones.
"""


from app.repositories.operaciones_repository import (
    add_operacion,
    get_operacion,
    obtener_operaciones,
    delete_operacion,
    delete_all_operaciones,
)

from app.repositories.tickers_repository import (
    validar_ticker,
)

from app.services.liquidez_service import (
    obtener_importe_liquidez,
    establecer_liquidez
)

"Crear una operación de compra/venta"
def crear_operacion(datos):

    validar_operacion(datos)

    if datos.tipo == "venta":
        validar_venta(datos)

    importe = (
        datos.titulos * datos.precio + datos.comision
        if datos.tipo == "compra"
        else datos.titulos * datos.precio - datos.comision
    )

    if datos.tipo == "compra" and importe > obtener_importe_liquidez(datos.usuario):
        raise ValueError(
            "La liquidez no es suficiente para realizar la compra."
        )

    operacion = add_operacion(
        usuario=datos.usuario,
        tipo=datos.tipo,
        ticker=datos.ticker,
        fecha=datos.fecha,
        titulos=datos.titulos,
        precio=datos.precio,
        comision=datos.comision,
        moneda=datos.moneda,
    )

    actualizar_liquidez_operacion(
        usuario=datos.usuario,
        tipo=datos.tipo,
        importe= importe,
    )

    return operacion

"Validar que los datos son coherentes"
def validar_operacion(datos):

    validar_ticker(datos.ticker)

    if datos.titulos <= 0:
        raise ValueError(
            "Los títulos deben ser mayores que cero."
        )

    if datos.precio <= 0:
        raise ValueError(
            "El precio debe ser mayor que cero."
        )

    if datos.comision < 0:
        raise ValueError(
            "La comisión no puede ser negativa."
        )

"Obtener las operaciones de un usuario"
def get_operaciones_usuario(usuario: str):

    operaciones = obtener_operaciones(usuario)

    operaciones = sorted(
        operaciones,
        key=lambda operacion: operacion["fecha"],
        reverse=True,
    )

    return {
        "ok": True,
        "datos": operaciones,
    }


"Borrar una operación"
def borrar_operacion(
    usuario: str,
    operacion_id: int,
    ):

    operacion = get_operacion(
        usuario,
        operacion_id,
    )

    if operacion is None:
        raise ValueError(
            "La operación no existe."
        )

    validar_borrado_operacion(
        usuario,
        operacion_id,
    )

    tipo = operacion["tipo"]

    if tipo == "compra":
        actualizar_liquidez_operacion(
            usuario=usuario,
            tipo="venta",
            importe=(
                operacion["titulos"] * operacion["precio"]
                + operacion["comision"]
            ),
        )
    elif tipo == "venta":
        actualizar_liquidez_operacion(
            usuario=usuario,
            tipo="compra",
            importe=(
                operacion["titulos"] * operacion["precio"]
                - operacion["comision"]
            ),
        )
    else:
        raise ValueError(
            f"Tipo de movimiento no válido: {tipo}"
        )

    return delete_operacion(
        usuario,
        operacion_id,
    )

"Solo se puede borra la última operación de un titulo"
def validar_borrado_operacion(
    usuario: str,
    operacion_id: int,
    ):

    operacion = get_operacion(
        usuario,
        operacion_id,
    )

    if operacion is None:
        raise ValueError(
            "La operación no existe."
        )

    operaciones = obtener_operaciones(usuario)

    operaciones = [
        op
        for op in operaciones
        if op["ticker"] == operacion["ticker"]
    ]

    operaciones.sort(
        key=lambda op: (
            op["fecha"],
            op["id"],
        )
    )

    ultima = operaciones[-1]

    if ultima["id"] != operacion_id:

        raise ValueError(
            "Solo se puede borrar la última operación de este valor."
        )



"Validamos que existan acciones para vender"
def validar_venta(datos):

    disponibles = obtener_titulos_disponibles(
        usuario=datos.usuario,
        ticker=datos.ticker,
    )

    if datos.titulos > disponibles:

        raise ValueError(
            (
                f"No dispone de suficientes títulos de "
                f"{datos.ticker}. "
                f"Disponibles: {disponibles}"
            )
        )

"Número de acciones en cartera de un titulo"
def obtener_titulos_disponibles(
    usuario: str,
    ticker: str,
) -> float:

    operaciones = obtener_operaciones(usuario)

    disponibles = 0

    for operacion in operaciones:

        if operacion["ticker"] != ticker:
            continue

        if operacion["tipo"] == "compra":
            disponibles += operacion["titulos"]

        elif operacion["tipo"] == "venta":
            disponibles -= operacion["titulos"]

    return disponibles

def actualizar_liquidez_operacion(usuario: str, tipo: str, importe: float):

    liquidez_actual = obtener_importe_liquidez(usuario)

    if tipo == "venta":
        nueva_liquidez = (
            liquidez_actual + importe
        )

    elif tipo == "compra":
        nueva_liquidez = (
            liquidez_actual - importe
        )

    else:
        raise ValueError(
            f"Tipo de movimiento no válido: {tipo}"
        )

    # 4. Guardar nueva liquidez
    establecer_liquidez(
        usuario=usuario,
        importe=nueva_liquidez,
        moneda="EUR",
    )
    
""" 
    Borrado de todas las operaciones de un usuario, 
    uso principal en las pruebas de rgresión
"""
def borrar_todas_operaciones(usuario: str):

    delete_all_operaciones(usuario)