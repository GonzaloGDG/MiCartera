# Ahorro y liquidez

## Propósito

Este nodo cubre la parte financiera de caja del sistema: ahorro personal, movimientos asociados y liquidez disponible.

## Ficheros clave

- [backend/app/routes/ahorro.py](../../../backend/app/routes/ahorro.py)
- [backend/app/routes/liquidez.py](../../../backend/app/routes/liquidez.py)
- [backend/app/services/ahorro_service.py](../../../backend/app/services/ahorro_service.py)
- [backend/app/services/liquidez_service.py](../../../backend/app/services/liquidez_service.py)
- [backend/app/schemas/ahorro.py](../../../backend/app/schemas/ahorro.py)
- [backend/app/schemas/liquidez.py](../../../backend/app/schemas/liquidez.py)
- [backend/app/data/movimientos_ahorro.json](../../../backend/app/data/movimientos_ahorro.json)
- [backend/app/data/liquidez.json](../../../backend/app/data/liquidez.json)

## Flujo principal

1. El frontend consulta el ahorro y la liquidez del usuario.
2. Se obtiene la suma de movimientos del ahorro.
3. Se obtiene el importe disponible de liquidez.
4. Los movimientos pueden crearse o borrarse.
5. La respuesta se devuelve con el total de liquidez asociado.

## Regla de negocio

- `ahorro` representa movimientos de caja o ahorro
- `liquidez` representa el saldo de efectivo disponible
- ambas entidades están relacionadas en la API de ahorro

## Dependencias

- [data.md](data.md)
- [frontend.md](frontend.md)
- [portfolio.md](portfolio.md)

## Cuándo leer este nodo

Cuando se toca:

- saldo de caja
- movimientos de ahorro
- ajustar liquidez disponible
- métricas financieras del usuario

## Riesgos

- la lógica de sincronización entre ahorro y liquidez debe mantenerse consistente
- el flujo actual depende de archivos JSON locales
