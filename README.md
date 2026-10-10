# MiCartera

Aplicación web para gestionar una cartera de inversión. El proyecto activo utiliza FastAPI en el backend y HTML, CSS y JavaScript en el frontend. `CarteraSoloHTML/` es un prototipo legacy.

## Estructura

- `backend/`: API, lógica de negocio, repositorios, datos y pruebas.
- `frontend/`: interfaz web estática.
- `docs/`: documentación funcional y técnica.
- `docker-compose.yml`: configuración de servicios Docker.

## Pruebas de regresión del backend

Ejecuta la batería completa después de cambiar lógica de negocio, servicios, repositorios, rutas, esquemas o datos del backend. Cubre autenticación, liquidez, ahorro, operaciones, cartera/FIFO, cotizaciones simuladas, tickers y el estado básico de la API.

Desde la raíz del repositorio, prepara el entorno local una sola vez:

```bash
cd backend
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Después de cada cambio, activa el entorno si hace falta y ejecuta toda la batería:

```bash
cd backend
. .venv/bin/activate
python -m pytest -q app/tests
```

Para ejecutar solo el flujo integrado principal:

```bash
cd backend
. .venv/bin/activate
python -m pytest -q app/tests/test_regresion.py
```

Los tests usan datos JSON temporales para no alterar los datos del proyecto y simulan las respuestas de Yahoo Finance, por lo que no necesitan conexión externa. La validación se considera correcta si pytest termina sin fallos (código de salida `0`). Si una prueba falla, corrige el problema antes de integrar el cambio.

Consulta [la documentación de pruebas](docs/knowledge/nodes/tests.md) para ver qué flujos cubre actualmente la batería y cuándo ejecutarla.
