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
- [frontend/components/navbar.js](../../../frontend/components/navbar.js)
- [frontend/css](../../../frontend/css)

## Flujo principal

- la pantalla de login envía credenciales a `/api/login`
- la vista de cartera consume `/api/cartera`
- la vista de ahorro consulta `/api/ahorro`
- la UI maneja errores y renderiza resultados en HTML

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

## Riesgos

- hay lógica de negocio parcialmente mezclada con la interfaz
- depende de los endpoints del backend y del formato exacto de respuestas
