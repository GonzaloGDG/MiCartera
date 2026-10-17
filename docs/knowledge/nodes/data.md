# Datos y modelos

## Propósito

Describe la capa de persistencia y modelos de dominio del proyecto. Los datos actuales viven en archivos JSON dentro de `backend/app/data/`.

## Ficheros clave

- [backend/app/data/usuarios.json](../../../backend/app/data/usuarios.json)
- [backend/app/data/operaciones.json](../../../backend/app/data/operaciones.json)
- [backend/app/data/liquidez.json](../../../backend/app/data/liquidez.json)
- [backend/app/data/movimientos_ahorro.json](../../../backend/app/data/movimientos_ahorro.json)
- [backend/app/data/tickers.json](../../../backend/app/data/tickers.json)
- [backend/app/schemas](../../../backend/app/schemas)

## Modelos de dominio

El proyecto usa Pydantic para validar la entrada y salida de la API. La lógica principal se apoya en:

- usuarios
- operaciones
- tickers
- ahorro
- liquidez
- cartera

Cada registro de `operaciones.json` conserva `id`, `usuario`, `tipo`, `ticker`, `fecha`, `titulos`, `precio`, `comision` y `moneda`. Los tipos admitidos son `compra`, `venta` y `dividendo`; la confirmación de compra a precio cero es un dato de solicitud y no forma parte del registro persistido. El resumen de inversión agrega solo compras en EUR.

## Dependencias

- [auth.md](auth.md)
- [portfolio.md](portfolio.md)
- [operations.md](operations.md)
- [ahorro.md](ahorro.md)

## Cuándo leer este nodo

Cuando se toca:

- formato JSON de persistencia
- modelos de respuesta
- validación de esquemas
- compatibilidad de datos con la pantalla o la API

## Riesgos

- el acceso a datos usa JSON local, no base de datos
- cualquier cambio en formato puede romper varios módulos del sistema

## Pruebas de regresión

- [conftest.py](../../../backend/app/tests/conftest.py): cada prueba ejecuta contra archivos JSON temporales, aislados y sembrados con datos mínimos; no modifica los datos de ejemplo del repositorio.
- [test_ahorro.py](../../../backend/app/tests/test_ahorro.py) y [test_operaciones.py](../../../backend/app/tests/test_operaciones.py): comprueban que entradas rechazadas no se persistan y que los cambios válidos queden almacenados.
- [test_operaciones.py](../../../backend/app/tests/test_operaciones.py): también valida el impacto y la reversión de liquidez por moneda, el resumen de compras en EUR y las reglas de títulos de ventas y dividendos.
- [test_tickers.py](../../../backend/app/tests/test_tickers.py): comprueba la persistencia parcial del actualizador cuando falla una cotización.

Ejecutar toda la batería con `cd backend && python -m pytest -q app/tests`.
