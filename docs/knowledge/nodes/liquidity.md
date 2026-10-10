# Liquidez

## Propósito

Representa el flujo de cálculo y modificación del importe líquido asociado a un usuario.

## Ficheros clave

- [backend/app/routes/liquidez.py](../../../backend/app/routes/liquidez.py)
- [backend/app/services/liquidez_service.py](../../../backend/app/services/liquidez_service.py)
- [backend/app/schemas/liquidez.py](../../../backend/app/schemas/liquidez.py)
- [backend/app/data/liquidez.json](../../../backend/app/data/liquidez.json)

## Flujo principal

- GET `/api/liquidez` devuelve el importe del usuario.
- PUT `/api/liquidez` modifica el importe y la moneda asociada.

## Regla de negocio

La liquidez está modelada como un dato de cuenta del usuario, distinto de las posiciones de inversión y del ahorro histórico.

## Dependencias

- [ahorro.md](ahorro.md)
- [data.md](data.md)
- [frontend.md](frontend.md)

## Cuándo leer este nodo

Cuando se cambia:

- saldo disponible
- moneda de referencia
- actualización manual de liquidez
- cálculo de recursos disponibles
