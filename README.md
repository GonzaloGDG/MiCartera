# MiCartera

Aplicación web para gestionar una cartera de inversión. El proyecto activo utiliza FastAPI en el backend y HTML, CSS y JavaScript en el frontend. `CarteraSoloHTML/` es un prototipo legacy.

## Cómo levantar el backend

Desde la raíz del repositorio, arranca el backend con Docker Compose:

```bash
docker compose up --build backend
```

Cuando Uvicorn indique que está listo, la API estará disponible en <http://localhost:8000> y la documentación interactiva en <http://localhost:8000/docs>. Para detenerlo, pulsa `Ctrl+C`; también puedes ejecutar `docker compose down`.

Como alternativa, para ejecutarlo directamente en el equipo sin Docker:

```bash
cd backend
. .venv/bin/activate
uvicorn app.main:app --reload
```

El entorno virtual `.venv` se crea e instala una sola vez siguiendo los pasos de preparación indicados en «Pruebas de regresión del backend».

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

## Pruebas E2E del frontend

Las pruebas de navegador usan Playwright y recorren los flujos de login, ahorro/liquidez, cartera y páginas provisionales. Para prepararlas:

```bash
cd frontend
npm install
npx playwright install chromium
```

Después, ejecútalas con:

```bash
cd frontend
npm test
```

Las respuestas de API se simulan durante estas pruebas: no hace falta iniciar el backend ni conectarse a Yahoo Finance. Consulta [la cobertura E2E](docs/knowledge/nodes/tests.md#pruebas-e2e-del-frontend).
