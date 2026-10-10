# Infraestructura

## Propósito

Describe la capa de ejecución del proyecto: contenedores, puertos y ejecución local de la API.

## Ficheros clave

- [docker-compose.yml](../../../docker-compose.yml)
- [backend/Dockerfile](../../../backend/Dockerfile)
- [backend/requirements.txt](../../../backend/requirements.txt)

## Configuración actual

El proyecto crea un servicio backend con:

- contexto: `./backend`
- container name: `micartera-backend`
- puerto: `8000:8000`
- volumen: `./backend:/app`
- comando: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

## Dependencias

- [architecture.md](architecture.md)
- [quotes.md](quotes.md)
- [frontend.md](frontend.md)

## Cuándo leer este nodo

Cuando se toca:

- Docker / Compose
- puertos
- entorno de ejecución
- dependencias Python
- despliegue local o de pruebas

## Riesgos

- la configuración actual es muy simple y depende de una estructura concreta del backend
- interesa mantener la configuración reproducible antes de introducir servicios adicionales

## Pruebas de regresión

- [test_infrastructure.py](../../../backend/app/tests/test_infrastructure.py): comprueba que la aplicación FastAPI arranque en el cliente de pruebas y que la ruta raíz informe estado `OK`.
- [test_cotizaciones.py](../../../backend/app/tests/test_cotizaciones.py): valida el uso del proveedor externo con Yahoo simulado, sin depender de la red.
- [playwright.config.js](../../../frontend/playwright.config.js): levanta un servidor estático local para las pruebas E2E; Playwright requiere instalar Chromium una vez.

Ejecutar con `cd backend && python -m pytest -q app/tests/test_infrastructure.py app/tests/test_cotizaciones.py`. El arranque de Docker Compose todavía no está cubierto por pruebas automatizadas.