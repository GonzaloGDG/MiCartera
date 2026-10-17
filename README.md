# MiCartera

Aplicación web para gestionar una cartera de inversión en bolsa.

El proyecto activo está formado por un backend en FastAPI y un frontend estático con HTML, CSS y JavaScript. La carpeta `CarteraSoloHTML/` se considera un prototipo legacy y no forma parte del desarrollo activo.

## 1. Objetivo

MiCartera permite consultar cotizaciones, visualizar la cartera y realizar seguimiento de inversiones.

El objetivo es desarrollar una aplicación modular, mantenible y fácil de ampliar.

## 2. Tecnologías

- Backend: Python y FastAPI.
- Frontend: HTML, CSS y JavaScript estáticos.
- Contenedores: Docker y Docker Compose.
- Control de versiones: Git.
- Entorno de desarrollo: Linux Mint y VS Code.
- IA de desarrollo: GitHub Copilot.

La incorporación de PostgreSQL está prevista, pero no debe darse por implementada hasta comprobarlo en el código actual.

## 3. Arquitectura

El proyecto activo está formado por el backend en `backend/` y el frontend estático en `frontend/`.

### Backend

- Aplicación basada en FastAPI.
- Punto de entrada: `backend/app/main.py`.
- API REST con rutas para autenticación, cartera, cotizaciones, liquidez, ahorro, operaciones y tickers.
- Organización por rutas, servicios, repositorios, esquemas y tareas de actualización.
- Los datos de ejemplo viven en `backend/app/data/`.
- Mantener separadas las rutas, la lógica de negocio y el acceso a datos.

### Frontend

- Aplicación web con HTML, CSS y JavaScript.
- Páginas principales: `login.html`, `cartera.html`, `ahorro.html` y `operaciones.html`.
- Archivos compartidos en `frontend/components/`, `frontend/css/` y `frontend/js/`.
- Consume la API del backend mediante peticiones HTTP.
- Mantener separada la interfaz de la lógica de negocio.
- Evitar duplicar código JavaScript.

### Docker

- Utilizar Docker Compose para gestionar los servicios.
- Actualmente el servicio principal es backend con Uvicorn en el puerto 8000.
- Mantener configuraciones reproducibles.
- No introducir dependencias innecesarias.
- Revisar puertos, volúmenes y variables de entorno antes de modificar la configuración.

## 4. Cómo levantar el backend

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

## 5. Estructura

- `backend/`: API, lógica de negocio, repositorios, datos y pruebas.
- `frontend/`: interfaz web estática.
- `docs/`: documentación funcional y técnica.
- `docker-compose.yml`: configuración de servicios Docker.
- `CarteraSoloHTML/`: prototipo legacy.

## 6. Instrucciones de desarrollo

- Antes de modificar archivos, inspeccionar el código existente y comprender su funcionamiento.
- Respetar la arquitectura y las convenciones actuales.
- Evitar reescribir componentes que ya funcionan.
- Proponer cambios pequeños y progresivos.
- No introducir librerías nuevas sin justificar su necesidad.
- No inventar endpoints, funciones ni estructuras que no existan en el proyecto.
- Si falta información, preguntar antes de asumir.
- Explicar brevemente los cambios realizados.

## 7. Python y FastAPI

- Utilizar código claro, legible y modular.
- Preferir funciones pequeñas con responsabilidades bien definidas.
- Utilizar anotaciones de tipos cuando aporten claridad.
- Gestionar correctamente las excepciones.
- Validar los datos recibidos por la API.
- Utilizar los mecanismos de validación de FastAPI y Pydantic cuando corresponda.
- Mantener la lógica de negocio fuera de las rutas cuando la complejidad lo justifique.

## 8. Frontend

- Mantener compatibilidad con los navegadores modernos.
- Utilizar JavaScript estándar salvo que exista una razón para añadir un framework.
- Gestionar los errores de las peticiones a la API.
- No almacenar contraseñas ni secretos en el frontend.
- Mantener una interfaz sencilla y coherente.

## 9. Seguridad

- No incluir contraseñas, tokens ni claves API directamente en el código.
- Utilizar variables de entorno para los secretos.
- Validar y sanear las entradas del usuario.
- No exponer información sensible en los logs.
- Revisar CORS y autenticación antes de desplegar la aplicación en producción.

## 10. Pruebas y validación

- Añadir pruebas cuando se incorporen funcionalidades.
- Ejecutar las pruebas existentes después de modificar el código.
- Comprobar que los endpoints responden correctamente.
- Verificar que los servicios Docker arrancan correctamente cuando se modifica su configuración.
- No afirmar que una prueba ha pasado si no se ha ejecutado realmente.

### Pruebas de regresión del backend

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

### Pruebas E2E del frontend

Las pruebas de navegador usan Playwright y recorren los flujos de login, ahorro/liquidez, cartera, operaciones y páginas provisionales. Para prepararlas:

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

Las respuestas de API se simulan durante estas pruebas: no hace falta iniciar el backend ni conectarse a Yahoo Finance. La cobertura de operaciones incluye compra a precio cero con confirmación, registro de dividendo con los títulos disponibles, selección de ticker para venta y borrado de la última operación. Consulta [la cobertura E2E](docs/knowledge/nodes/tests.md#pruebas-e2e-del-frontend).

## 11. Forma de trabajar del asistente

- Responder en español.
- Ser conciso y explicar los pasos de forma ordenada.
- Priorizar soluciones sencillas y comprensibles.
- Para cambios importantes, dividir el trabajo en pasos pequeños.
- Antes de realizar modificaciones amplias, presentar un resumen del enfoque.
- Mostrar los archivos afectados y explicar qué se ha cambiado.
- No modificar archivos ajenos a la tarea solicitada.

## 12. Desarrollo guiado por especificación (SDD)

Se recomienda usar SDD como metodología principal para continuar el desarrollo del proyecto. En este contexto, SDD significa definir primero la funcionalidad deseada, validarla con criterios concretos y luego implementarla con la menor complejidad posible.

### Flujo recomendado

1. Definir el problema y el objetivo.
   - Qué debe hacer la funcionalidad.
   - Qué casos se contemplan.
   - Qué comportamiento debe evitarse.

2. Crear una especificación breve.
   - Describir la entrada, la lógica y la salida esperada.
   - Añadir criterios de aceptación claros y verificables.
   - Situar la funcionalidad dentro del contexto del backend o frontend.

3. Diseñar la solución mínima.
   - Identificar qué rutas, servicios, repositorios o componentes se ven afectados.
   - Mantener la estructura actual del proyecto.
   - Evitar cambios innecesarios o ampliaciones no justificadas.

4. Implementar con validación incremental.
   - Realizar el cambio de forma pequeña y comprobable.
   - Ejecutar las pruebas relevantes antes de cerrar la tarea.

5. Revisar y documentar.
   - Confirmar que la funcionalidad cumple la especificación.
   - Actualizar documentación si el cambio afecta el comportamiento del sistema.

### Regla práctica

La mejor combinación para este proyecto es SDD + TDD:
- SDD define qué debe hacerse.
- TDD valida que la implementación cumple esa definición.

Esto mantiene un desarrollo más robusto, más fácil de revisar y más mantenible a largo plazo.

## 13. Estado del proyecto

Este apartado debe mantenerse actualizado.

Antes de proponer cambios, revisar el estado real del repositorio, los archivos y la configuración.

El desarrollo activo se centra en la estructura de `backend/` y `frontend/`. La carpeta `CarteraSoloHTML` es un proyecto antiguo o de prueba, no un módulo activo del sistema principal.

No asumir que las funcionalidades descritas en la documentación ya están implementadas.
