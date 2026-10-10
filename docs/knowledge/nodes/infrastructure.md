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