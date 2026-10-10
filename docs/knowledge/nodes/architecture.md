# Arquitectura general

## Propósito

Este nodo describe la estructura global del proyecto activo de MiCartera y cómo se articulan backend, frontend y datos.

## Alcance

- FastAPI como API principal
- Frontend estático en HTML/CSS/JS
- Datos persistidos en JSON dentro de `backend/app/data/`
- Docker Compose para levantar la API

## Ficheros clave

- [backend/app/main.py](../../../backend/app/main.py)
- [backend/app/routes](../../../backend/app/routes)
- [backend/app/services](../../../backend/app/services)
- [backend/app/repositories](../../../backend/app/repositories)
- [backend/app/data](../../../backend/app/data)
- [frontend](../../../frontend)
- [docker-compose.yml](../../../docker-compose.yml)

## Módulos principales

### Backend

La aplicación se monta en `backend/app/main.py` y registra los routers de:

- autenticación
- cartera
- cotizaciones
- liquidez
- ahorro
- operaciones
- tickers

La API usa CORS abierto para desarrollo y expone varios endpoints bajo el prefijo `/api`.

### Frontend

La interfaz se distribuye en:

- `frontend/login.html`
- `frontend/cartera.html`
- `frontend/ahorro.html`
- `frontend/js/`
- `frontend/css/`
- `frontend/components/`

### Datos

Los datos de prueba están en JSON bajo `backend/app/data/` y se consumen desde los repositorios.

## Dependencias entre capas

- rutas -> servicios -> repositorios -> JSON
- servicios -> proveedores externos (por ejemplo Yahoo Finance)
- frontend -> API REST (HTTP)

## Puntos de cuidado

- no mezclar lógica de negocio en rutas
- respetar la separación entre serialización y acceso a datos
- evitar asumir que la carpeta legacy es parte del proyecto activo

## Nodos relacionados

- [auth.md](auth.md)
- [portfolio.md](portfolio.md)
- [quotes.md](quotes.md)
- [data.md](data.md)
- [infrastructure.md](infrastructure.md)

## Validación de regresión

Al modificar un dominio backend, ejecutar las pruebas enlazadas en su nodo. Como comprobación integral de cambios en servicios, rutas, repositorios o persistencia, ejecutar la suite completa: `cd backend && python -m pytest -q app/tests`. El alcance actual está detallado en [tests.md](tests.md).
