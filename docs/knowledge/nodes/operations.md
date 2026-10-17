# Operaciones

## Propósito

Gestiona las compras, ventas y dividendos del usuario, el resumen de inversión y la lista y eliminación de operaciones.

## Ficheros clave

- [backend/app/routes/operaciones.py](../../../backend/app/routes/operaciones.py)
- [backend/app/services/operaciones_service.py](../../../backend/app/services/operaciones_service.py)
- [backend/app/schemas/operaciones.py](../../../backend/app/schemas/operaciones.py)
- [backend/app/data/operaciones.json](../../../backend/app/data/operaciones.json)
- [backend/app/repositories/operaciones_repository.py](../../../backend/app/repositories/operaciones_repository.py)
- [frontend/operaciones.html](../../../frontend/operaciones.html)
- [frontend/js/operaciones.js](../../../frontend/js/operaciones.js)
- [frontend/css/operaciones.css](../../../frontend/css/operaciones.css)
- [frontend/tests/e2e/operaciones.spec.js](../../../frontend/tests/e2e/operaciones.spec.js)

## Flujo principal

1. La vista carga las operaciones del usuario y el catálogo desde `GET /api/operaciones` y `GET /api/tickers`.
2. El usuario registra una compra, venta o dividendo desde el formulario; el servicio centraliza la validación y el repositorio persiste la operación en `operaciones.json`.
3. La liquidez se actualiza en la misma moneda de la operación: compra resta el importe con comisión; venta y dividendo suman el importe neto.
4. El resumen presenta el total invertido y los últimos seis años de compras en EUR, con variación anual respecto al año anterior. Las demás monedas se muestran en el historial, pero no se convierten ni agregan al resumen.
5. El borrado revierte el impacto de liquidez y solo se permite para la última operación del ticker del usuario.

## Regla de negocio

El sistema centraliza las operaciones para calcular posiciones abiertas y costes con FIFO. Las ventas no pueden superar los títulos disponibles. Los dividendos requieren una posición abierta y el número de títulos debe coincidir con el total disponible. Una compra con precio cero exige confirmación explícita.

La interfaz obtiene el usuario de la sesión, permite elegir moneda, muestra la información de las operaciones y requiere confirmación antes de registrar una compra a precio cero o borrar una operación.

## API implicada

- `GET /api/operaciones?usuario=<usuario>`: devuelve las operaciones y el resumen EUR.
- `POST /api/operaciones`: registra una operación.
- `DELETE /api/operaciones/{id}?usuario=<usuario>`: elimina la última operación del ticker y revierte su impacto en liquidez.
- `GET /api/tickers`: proporciona el catálogo para el selector.

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

- [test_operaciones.py](../../../backend/app/tests/test_operaciones.py): cubre compra, venta, dividendo, creación/borrado por API, liquidez por moneda, resumen de seis años en EUR, confirmación de precio cero, títulos disponibles, validaciones y reversión al borrar.
- [test_cartera.py](../../../backend/app/tests/test_cartera.py): valida FIFO con operaciones de compra y venta.
- [test_regresion.py](../../../backend/app/tests/test_regresion.py): comprueba conjuntamente ingreso de ahorro, compra y borrado.
- [operaciones.spec.js](../../../frontend/tests/e2e/operaciones.spec.js): comprueba el resumen, compra a precio cero confirmada, selección de ticker y títulos para dividendo y venta, y eliminación de la última operación desde la vista.

Ejecutar backend con `cd backend && python -m pytest -q app/tests/test_operaciones.py app/tests/test_cartera.py app/tests/test_regresion.py` y E2E con `cd frontend && npx playwright test tests/e2e/operaciones.spec.js`.