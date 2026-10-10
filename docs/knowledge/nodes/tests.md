# Pruebas

## Propósito

Documenta la cobertura actual de pruebas y el enfoque de validación del proyecto.

## Ficheros clave

- [backend/app/tests/helpers.py](../../../backend/app/tests/helpers.py)
- [backend/app/tests/test_regresion.py](../../../backend/app/tests/test_regresion.py)
- [backend/app/tests/__init__.py](../../../backend/app/tests/__init__.py)

## Qué cubren las pruebas actuales

El proyecto incluye una batería de pruebas orientadas a regresión, con foco en la coherencia funcional del backend.

## Dependencias

- [architecture.md](architecture.md)
- [portfolio.md](portfolio.md)
- [operations.md](operations.md)
- [quotes.md](quotes.md)

## Cuándo leer este nodo

Cuando se está desarrollando o validando:

- un cambio funcional importante
- una regresión
- una corrección de endpoints o negocio
- una actualización de datos

## Riesgos

- la cobertura debe ampliarse a medida que aumente la complejidad del sistema
- conviene mantener pruebas para cada dominio importante del negocio
