# Pruebas

## Propósito

Documenta la cobertura actual de pruebas y el enfoque de validación del proyecto. Este nodo sirve como checklist operativo para comprobar que un cambio funcional no rompe el backend.

## Ficheros clave

- [backend/app/tests/conftest.py](../../../backend/app/tests/conftest.py)
- [backend/app/tests/helpers.py](../../../backend/app/tests/helpers.py)
- [backend/app/tests/test_regresion.py](../../../backend/app/tests/test_regresion.py)
- [backend/app/tests](../../../backend/app/tests)
- [frontend/package.json](../../../frontend/package.json)
- [frontend/playwright.config.js](../../../frontend/playwright.config.js)
- [frontend/tests/e2e](../../../frontend/tests/e2e)

## Qué cubren las pruebas actuales

La batería cubre autenticación, liquidez, ahorro, operaciones, cartera/FIFO, cotizaciones Yahoo, catálogo de tickers y el estado básico de la API. Las llamadas externas a Yahoo Finance se simulan; la suite no depende de la red.

Cada prueba utiliza archivos JSON temporales mediante `conftest.py`; no modifica los datos reales guardados en `backend/app/data/`.

Pruebas por dominio:

- `test_auth.py`: login válido y credenciales incorrectas.
- `test_liquidez.py`: consulta, actualización, alta de cuenta y saldo negativo.
- `test_ahorro.py`: ingresos, retiradas, borrado, totales anuales y validación de entradas.
- `test_operaciones.py`: compras, ventas, liquidez, títulos, borrado y validaciones.
- `test_cartera.py`: coste FIFO, valoración y operaciones inconsistentes.
- `test_cotizaciones.py`: respuesta de cotización e histórico y proveedor simulado.
- `test_tickers.py`: orden del catálogo y actualización parcial ante fallos externos.
- `test_infrastructure.py`: respuesta de salud de la ruta raíz.
- `test_regresion.py`: flujo integrado de ingreso, compra y borrado.

## Validación mínima antes de aceptar un cambio

Al modificar lógica de negocio, servicios, repositorios, rutas, esquemas o datos del backend, ejecutar la batería completa:

```bash
cd backend
. .venv/bin/activate
python -m pytest -q app/tests
```

Para preparar el entorno aislado una sola vez:

```bash
cd backend
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Para lanzar una prueba o dominio concreto, por ejemplo:

```bash
cd backend
. .venv/bin/activate
python -m pytest -q app/tests/test_operaciones.py app/tests/test_cartera.py
```

## Pruebas E2E del frontend

Las pruebas de Playwright usan Chromium y navegan la interfaz en un navegador real. La API se simula con interceptores para tener respuestas repetibles; no requieren backend activo, credenciales reales ni acceso a Yahoo Finance.

Preparación inicial:

```bash
cd frontend
npm install
npx playwright install chromium
```

Ejecución:

```bash
cd frontend
npm test
```

Flujos cubiertos:

- `auth.spec.js`: login correcto conserva y consulta con el username autenticado; login incorrecto muestra el error; una página protegida redirige al login.
- `ahorro.spec.js`: registro y borrado de ingreso y retirada, actualización manual de liquidez, totales anuales dinámicos y presentación del detalle de error de API.
- `cartera.spec.js`: usuario correcto en la consulta, totales de cartera, fecha de actualización del servidor, renderizado seguro de datos y aviso de páginas aún no implementadas.

Estas pruebas validan la interacción y presentación en navegador. Las reglas de negocio y persistencia se siguen validando con pytest en el backend. No sustituyen pruebas integradas con backend real.

## Cuándo ejecutar estas pruebas

Conviene lanzar la validación cuando se está desarrollando o corrigiendo:

- un cambio funcional importante
- una regresión
- una corrección de endpoints o negocio
- una modificación de repositorios o ficheros JSON
- cambios en liquidez, ahorro, cartera o operaciones
- cambios en autenticación, cotizaciones o catálogo de tickers
- actualización de dependencias o configuración del backend
- cambios en login, navegación, formularios o renderizado del frontend (ejecutar también Playwright)

## Resultado esperado

La validación debe terminar con código de salida `0` y mostrar todos los tests como aprobados. La cantidad puede aumentar cuando se añadan nuevas regresiones.

## Dependencias

- [architecture.md](architecture.md)
- [portfolio.md](portfolio.md)
- [operations.md](operations.md)
- [quotes.md](quotes.md)

## Riesgos

- la suite verifica el comportamiento de la aplicación con datos simulados; no garantiza disponibilidad real de Yahoo Finance
- no se valida automáticamente el arranque de Docker Compose ni las llamadas a proveedores externos
- las pruebas Playwright simulan la API; no garantizan por sí solas la integración real frontend-backend
- conviene ampliar las regresiones cuando se incorporen nuevas funcionalidades
- si una prueba falla, no se debe mergear el cambio sin corregir el problema
