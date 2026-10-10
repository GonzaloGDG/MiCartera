# Cotizaciones

## Propósito

Gestiona la consulta de precios de mercado y el historial de un ticker, importando los datos desde Yahoo Finance.

## Ficheros clave

- [backend/app/routes/cotizaciones.py](../../../backend/app/routes/cotizaciones.py)
- [backend/app/services/cotizaciones_service.py](../../../backend/app/services/cotizaciones_service.py)
- [backend/app/providers/yahoo_finance.py](../../../backend/app/providers/yahoo_finance.py)
- [backend/app/tasks/ticker_updater.py](../../../backend/app/tasks/ticker_updater.py)
- [backend/app/schemas/cotizaciones.py](../../../backend/app/schemas/cotizaciones.py)

## Flujo principal

1. El frontend pide una cotización o un histórico para un ticker.
2. La ruta llama al servicio de cotizaciones.
3. El proveedor de Yahoo Finance obtiene el dato.
4. El task de actualización puede refrescar precios y guardarlos en JSON.

## Dependencias

- [tickers.md](tickers.md)
- [portfolio.md](portfolio.md)
- [infrastructure.md](infrastructure.md)

## Cuándo leer este nodo

Cuando se toca:

- actualización de precios
- histórico de cotización
- proveedor de datos externos
- ajustes del periodo e intervalo de consulta

## Riesgos

- dependencia externa a Yahoo Finance
- posibles errores si el ticker no existe o la API no devuelve datos
- actualización de precios debe mantenerse consistente con `tickers.json`
