"""
Lógica de negocio de operaciones.
"""

from datetime import date
from math import isclose, isfinite

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
    elif datos.tipo == "dividendo":
        validar_dividendo(datos)

    importe = importe_operacion(
        datos.tipo,
        datos.titulos,
        datos.precio,
        datos.comision,
    )

    moneda = datos.moneda.strip().upper()
    validar_saldo_operacion(
        usuario=datos.usuario,
        tipo=datos.tipo,
        importe=importe,
        moneda=moneda,
    )

    operacion = add_operacion(
        usuario=datos.usuario,
        tipo=datos.tipo,
        ticker=datos.ticker,
        fecha=datos.fecha,
        titulos=datos.titulos,
        precio=datos.precio,
        comision=datos.comision,
        moneda=moneda,
    )
    actualizar_liquidez_operacion(
        usuario=datos.usuario,
        tipo=datos.tipo,
        importe=importe,
        moneda=moneda,
    )

    return operacion


def importe_operacion(
    tipo: str,
    titulos: float,
    precio: float,
    comision: float,
) -> float:
    importe_bruto = titulos * precio
    if tipo == "compra":
        return importe_bruto + comision
    return importe_bruto - comision


"Validar que los datos son coherentes"
def validar_operacion(datos):

    validar_ticker(datos.ticker)

    if not datos.usuario.strip():
        raise ValueError("El usuario es obligatorio.")

    if datos.tipo not in {"compra", "venta", "dividendo"}:
        raise ValueError("El tipo de operación no es válido.")

    if datos.titulos <= 0:
        raise ValueError(
            "Los títulos deben ser mayores que cero."
        )
    if not isfinite(datos.titulos):
        raise ValueError("Los títulos deben ser un número finito.")

    if not isfinite(datos.precio):
        raise ValueError("El precio debe ser un número finito.")
    if datos.precio < 0:
        raise ValueError(
            "El precio no puede ser negativo."
        )

    if datos.precio == 0 and datos.tipo != "compra":
        raise ValueError(
            "El precio debe ser mayor que cero para ventas y dividendos."
        )

    if (
        datos.tipo == "compra"
        and datos.precio == 0
        and not datos.confirmar_precio_cero
    ):
        raise ValueError(
            "Confirme la compra a precio cero para registrar un posible dividendo en acciones."
        )

    if not isfinite(datos.comision):
        raise ValueError("La comisión debe ser un número finito.")
    if datos.comision < 0:
        raise ValueError(
            "La comisión no puede ser negativa."
        )

    if not datos.moneda.strip():
        raise ValueError("La moneda es obligatoria.")
    moneda = datos.moneda.strip()
    if len(moneda) != 3 or not moneda.isascii() or not moneda.isalpha():
        raise ValueError("La moneda debe ser un código ISO de tres letras.")

    try:
        date.fromisoformat(datos.fecha)
    except ValueError as error:
        raise ValueError(
            "La fecha debe tener el formato AAAA-MM-DD."
        ) from error


def validar_dividendo(datos):
    disponibles = obtener_titulos_disponibles(
        usuario=datos.usuario,
        ticker=datos.ticker,
    )
    if disponibles <= 0:
        raise ValueError(
            f"No dispone de títulos de {datos.ticker} para registrar el dividendo."
        )
    if not isclose(datos.titulos, disponibles, rel_tol=1e-9, abs_tol=1e-9):
        raise ValueError(
            f"Los títulos del dividendo deben coincidir con los disponibles ({disponibles})."
        )

"Obtener las operaciones de un usuario"
def get_operaciones_usuario(usuario: str):

    operaciones = obtener_operaciones(usuario)

    operaciones = sorted(
        operaciones,
        key=lambda operacion: operacion["fecha"],
        reverse=True,
    )

    año_actual = date.today().year
    años = list(range(año_actual - 5, año_actual + 1))
    compras_por_año = {}
    total_invertido = 0.0

    for operacion in operaciones:
        if operacion["tipo"] != "compra" or operacion["moneda"] != "EUR":
            continue
        importe = importe_operacion(
            "compra",
            operacion["titulos"],
            operacion["precio"],
            operacion["comision"],
        )
        total_invertido += importe
        try:
            año = date.fromisoformat(operacion["fecha"]).year
        except (TypeError, ValueError):
            continue
        compras_por_año[str(año)] = compras_por_año.get(str(año), 0.0) + importe

    resumen_anual = []
    for año in años:
        total = compras_por_año.get(str(año), 0.0)
        previo = compras_por_año.get(str(año - 1), 0.0)
        variacion = round((total - previo) / previo * 100, 2) if previo else 0
        resumen_anual.append({
            "año": año,
            "total": round(total, 2),
            "variacion": variacion,
        })

    return {
        "ok": True,
        "datos": operaciones,
        "moneda_resumen": "EUR",
        "total_invertido": round(total_invertido, 2),
        "totales_anuales": resumen_anual,
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
            importe=importe_operacion(
                "compra",
                operacion["titulos"],
                operacion["precio"],
                operacion["comision"],
            ),
            moneda=operacion["moneda"],
        )
    elif tipo in {"venta", "dividendo"}:
        actualizar_liquidez_operacion(
            usuario=usuario,
            tipo="compra",
            importe=importe_operacion(
                tipo,
                operacion["titulos"],
                operacion["precio"],
                operacion["comision"],
            ),
            moneda=operacion["moneda"],
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

def actualizar_liquidez_operacion(
    usuario: str,
    tipo: str,
    importe: float,
    moneda: str = "EUR",
):

    nueva_liquidez = calcular_nueva_liquidez(
        usuario,
        tipo,
        importe,
        moneda,
    )

    establecer_liquidez(
        usuario=usuario,
        importe=nueva_liquidez,
        moneda=moneda,
    )


def validar_saldo_operacion(
    usuario: str,
    tipo: str,
    importe: float,
    moneda: str,
):
    calcular_nueva_liquidez(usuario, tipo, importe, moneda)


def calcular_nueva_liquidez(
    usuario: str,
    tipo: str,
    importe: float,
    moneda: str,
) -> float:
    liquidez_actual = obtener_importe_liquidez(
        usuario,
        moneda=moneda,
        valor_por_defecto=0.0,
    )

    if tipo == "compra":
        nueva_liquidez = liquidez_actual - importe
    elif tipo in {"venta", "dividendo"}:
        nueva_liquidez = liquidez_actual + importe
    else:
        raise ValueError(f"Tipo de movimiento no válido: {tipo}")

    if nueva_liquidez < 0:
        raise ValueError(
            f"La liquidez {moneda} no es suficiente para realizar la operación."
        )

    return nueva_liquidez
    
""" 
    Borrado de todas las operaciones de un usuario, 
    uso principal en las pruebas de rgresión
"""
def borrar_todas_operaciones(usuario: str):

    delete_all_operaciones(usuario)