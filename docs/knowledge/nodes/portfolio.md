# Cartera

## Propósito

Muestra la cartera actual del usuario, a partir de posiciones abiertas y precios actuales de los tickers.

## Ficheros clave

- [backend/app/routes/cartera.py](../../../backend/app/routes/cartera.py)
- [backend/app/services/cartera_service.py](../../../backend/app/services/cartera_service.py)
- [backend/app/services/fifo_service.py](../../../backend/app/services/fifo_service.py)
- [backend/app/repositories/tickers_repository.py](../../../backend/app/repositories/tickers_repository.py)
- [backend/app/schemas/cartera.py](../../../backend/app/schemas/cartera.py)
- [frontend/js/cartera.js](../../../frontend/js/cartera.js)
- [frontend/cartera.html](../../../frontend/cartera.html)

## Flujo principal

1. El usuario solicita su cartera.
2. El servicio calcula posiciones abiertas con FIFO.
3. Se obtiene el catálogo de tickers.
4. Se calcula precio actual, coste total, diferencia y variación respecto a compra.
5. La respuesta se presenta al frontend.

## Regla de negocio

La cartera se calcula en función de:

- posiciones abiertas
- precio medio de compra
- número de títulos
- precio actual del ticker
- variación porcentual del ticker

## Dependencias

- [operations.md](operations.md)
- [tickers.md](tickers.md)
- [quotes.md](quotes.md)
- [data.md](data.md)

## Cuándo leer este nodo

Cuando se cambia:

- cálculo de valor de la cartera
- lógica FIFO
- visualización de posiciones
- precios actuales o diferencias de compra

## Riesgos

- la lógica depende heavily del contenido de `tickers.json`
- el modelo de posiciones puede no cubrir casos complejos de operaciones fraccionadas o históricas

## Pruebas de regresión

- [test_cartera.py](../../../backend/app/tests/test_cartera.py): comprueba el coste de lotes FIFO parcialmente vendidos, la valoración de cartera en la API y el rechazo de una venta sin compra previa en los datos.
- [test_operaciones.py](../../../backend/app/tests/test_operaciones.py): comprueba la disponibilidad de títulos antes de vender.

Ejecutar con `cd backend && python -m pytest -q app/tests/test_cartera.py app/tests/test_operaciones.py`.
