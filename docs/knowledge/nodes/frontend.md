# Frontend

## Propósito

Esta capa ofrece la interfaz web del sistema. Se construye con HTML, CSS y JavaScript vanilla, siguiendo una estructura simple sin framework.

## Ficheros clave

- [frontend/login.html](../../../frontend/login.html)
- [frontend/cartera.html](../../../frontend/cartera.html)
- [frontend/ahorro.html](../../../frontend/ahorro.html)
- [frontend/js/login.js](../../../frontend/js/login.js)
- [frontend/js/cartera.js](../../../frontend/js/cartera.js)
- [frontend/js/ahorro.js](../../../frontend/js/ahorro.js)
- [frontend/components/api.js](../../../frontend/components/api.js)
- [frontend/components/navbar.js](../../../frontend/components/navbar.js)
- [frontend/components/last-update.js](../../../frontend/components/last-update.js)
- [frontend/tests/e2e](../../../frontend/tests/e2e)
- [frontend/playwright.config.js](../../../frontend/playwright.config.js)
- [frontend/css](../../../frontend/css)

## Flujo principal

- la pantalla de login envía credenciales a `/api/login`
- la sesión conserva el `username` devuelto por el backend para identificar al usuario en las peticiones
- la vista de cartera consume `/api/cartera`
- la vista de ahorro consulta `/api/ahorro`
- la UI maneja errores y renderiza resultados como texto para no interpretar datos de API como HTML
- las marcas de actualización usan la fecha devuelta por el backend; no la hora local de renderizado
- las páginas de navegación aún no implementadas muestran un aviso temporal de página no disponible

## Dependencias

- [auth.md](auth.md)
- [portfolio.md](portfolio.md)
- [ahorro.md](ahorro.md)
- [infrastructure.md](infrastructure.md)

## Cuándo leer este nodo

Cuando se cambia:

- rediseño visual
- integración con APIs
- navegación
- formularios y tratamiento de errores del cliente

## Pruebas de regresión

Las pruebas E2E de Playwright cubren login e identidad de usuario, operaciones de ahorro/liquidez disponibles en la UI, cartera, fecha de actualización, manejo visible de errores y páginas provisionales. Ejecutar desde `frontend/` con `npm test`; la API se intercepta y simula, sin iniciar el backend.

## Riesgos

- hay lógica de negocio parcialmente mezclada con la interfaz
- depende de los endpoints del backend y del formato exacto de respuestas
