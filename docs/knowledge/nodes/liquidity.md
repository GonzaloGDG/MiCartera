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

## Pruebas de regresión

- [test_liquidez.py](../../../backend/app/tests/test_liquidez.py): valida consulta del saldo EUR, actualización y creación de una cuenta inexistente y rechazo de saldos negativos.
- [test_ahorro.py](../../../backend/app/tests/test_ahorro.py) y [test_operaciones.py](../../../backend/app/tests/test_operaciones.py): verifican que los movimientos de ahorro y las compras/ventas actualizan y revierten correctamente la liquidez.
- [ahorro.spec.js](../../../frontend/tests/e2e/ahorro.spec.js): valida la edición manual de liquidez y su reflejo visual en la interfaz.

Ejecutar con `cd backend && python -m pytest -q app/tests/test_liquidez.py app/tests/test_ahorro.py app/tests/test_operaciones.py`.
