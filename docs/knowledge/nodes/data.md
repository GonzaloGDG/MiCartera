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
