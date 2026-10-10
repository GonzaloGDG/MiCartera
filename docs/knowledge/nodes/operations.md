# Operaciones

## Propósito

Gestiona las compras y ventas de activos, así como la lista y eliminación de operaciones del usuario.

## Ficheros clave

- [backend/app/routes/operaciones.py](../../../backend/app/routes/operaciones.py)
- [backend/app/services/operaciones_service.py](../../../backend/app/services/operaciones_service.py)
- [backend/app/schemas/operaciones.py](../../../backend/app/schemas/operaciones.py)
- [backend/app/data/operaciones.json](../../../backend/app/data/operaciones.json)
- [backend/app/repositories/operaciones_repository.py](../../../backend/app/repositories/operaciones_repository.py)

## Flujo principal

1. Se recibe una operación con datos de compra/venta.
2. El servicio valida la operación.
3. Se registra en `operaciones.json` o se reutiliza la lógica de repositorio.
4. La operación afecta a la cartera y, por extensión, al cálculo de posiciones y diferencias.

## Regla de negocio

El sistema centraliza las operaciones para poder calcular posiciones abiertas y costes con FIFO.

## Dependencias

- [portfolio.md](portfolio.md)
- [data.md](data.md)
- [tickers.md](tickers.md)

## Cuándo leer este nodo

Cuando se toca:

- compra / venta de activos
- validación de operación
- borrado de registro
- cálculo de coste histórico

## Riesgos

- la validación es sensible a datos incompletos
- la lógica de operación puede estar acoplada a la forma del JSON de persistencia

## Pruebas de regresión

- [test_operaciones.py](../../../backend/app/tests/test_operaciones.py): cubre compra, venta, saldos y títulos, reversión al borrar, orden de listado, regla de borrar solo la última operación y rechazo de ticker, cantidad, precio, comisión, saldo o venta inválidos.
- [test_cartera.py](../../../backend/app/tests/test_cartera.py): valida FIFO con operaciones de compra y venta.
- [test_regresion.py](../../../backend/app/tests/test_regresion.py): comprueba conjuntamente ingreso de ahorro, compra y borrado.

Ejecutar con `cd backend && python -m pytest -q app/tests/test_operaciones.py app/tests/test_cartera.py app/tests/test_regresion.py`.