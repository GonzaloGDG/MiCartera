# Tickers

## Propósito

Define el catálogo de activos del proyecto. Aquí se gestionan los valores, su nombre, moneda, precio actual y fecha de última actualización.

## Ficheros clave

- [backend/app/routes/tickers.py](../../../backend/app/routes/tickers.py)
- [backend/app/services/tickers_service.py](../../../backend/app/services/tickers_service.py)
- [backend/app/repositories/tickers_repository.py](../../../backend/app/repositories/tickers_repository.py)
- [backend/app/data/tickers.json](../../../backend/app/data/tickers.json)
- [backend/app/tasks/ticker_updater.py](../../../backend/app/tasks/ticker_updater.py)

## Flujo principal

- el backend expone `/api/tickers`
- el servicio devuelve el catálogo de activos
- el actualizador de precios puede refrescar el valor de cada ticker

## Regla de negocio

Los tickers son la base de la cartera, de las cotizaciones y de los cálculos de rendimiento.

## Dependencias

- [quotes.md](quotes.md)
- [portfolio.md](portfolio.md)
- [data.md](data.md)

## Cuándo leer este nodo

Cuando se toca:

- catálogo de valores
- cambios de nombre, moneda o metadatos
- actualización automática de precios
- nuevo ticker o eliminación de uno existente
