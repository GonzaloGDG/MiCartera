# MiCartera - Índice de conocimiento

Este directorio recoge el contexto funcional y técnico del proyecto activo de MiCartera, excluyendo la carpeta legacy `CarteraSoloHTML`.

## Objetivo del proyecto

MiCartera es una aplicación web para gestionar una cartera de inversión en bolsa. El sistema permite:

- autenticar usuarios
- consultar la cartera actual
- registrar compras y ventas
- gestionar ahorro y liquidez
- consultar precios e histórico de tickers
- actualizar datos del mercado desde Yahoo Finance

## Vista general de la arquitectura

- Backend: FastAPI en `backend/app/`
- Frontend: HTML, CSS y JavaScript en `frontend/`
- Datos de ejemplo: `backend/app/data/`
- Docker: `docker-compose.yml`

## Nodos de conocimiento

- [Arquitectura general](nodes/architecture.md)
- [Autenticación](nodes/auth.md)
- [Cartera](nodes/portfolio.md)
- [Operaciones](nodes/operations.md)
- [Ahorro y liquidez](nodes/ahorro.md)
- [Liquidez](nodes/liquidity.md)
- [Cotizaciones](nodes/quotes.md)
- [Tickers](nodes/tickers.md)
- [Frontend](nodes/frontend.md)
- [Infraestructura](nodes/infrastructure.md)
- [Datos y modelos](nodes/data.md)
- [Pruebas](nodes/tests.md)

## Cómo usar este índice

- Si se va a tocar login o sesión: revisar [auth.md](nodes/auth.md)
- Si se va a modificar la pantalla o lógica de cartera: revisar [portfolio.md](nodes/portfolio.md)
- Si se va a cambiar la lógica de compra/venta: revisar [operations.md](nodes/operations.md)
- Si se va a ajustar precios o Yahoo Finance: revisar [quotes.md](nodes/quotes.md)
- Si se va a tocar persistence o archivos JSON: revisar [data.md](nodes/data.md)

## Ficheros relevantes del proyecto activo

- [backend/app/main.py](../../backend/app/main.py)
- [backend/app/routes](../../backend/app/routes)
- [backend/app/services](../../backend/app/services)
- [backend/app/repositories](../../backend/app/repositories)
- [backend/app/data](../../backend/app/data)
- [frontend](../../frontend)
- [docker-compose.yml](../../docker-compose.yml)

## Nota de alcance

La carpeta `CarteraSoloHTML` queda fuera del contexto activo de este índice. Se considera un prototipo o versión anterior y no debe tomarse como base de desarrollo principal.
