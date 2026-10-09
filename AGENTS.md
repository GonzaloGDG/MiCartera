
# MiCartera - Contexto del proyecto

## 1. Objetivo

MiCartera es una aplicación web para gestionar una
cartera de inversión en bolsa.

El proyecto permite consultar cotizaciones, visualizar
la cartera y realizar seguimiento de inversiones.

El objetivo es desarrollar una aplicación modular,
mantenible y fácil de ampliar.

## 2. Tecnologías

- Backend: Python y FastAPI.
- Frontend: HTML, CSS y JavaScript estáticos.
- Contenedores: Docker y Docker Compose.
- Control de versiones: Git.
- Entorno de desarrollo: Linux Mint y VS Code.
- IA de desarrollo: GitHub Copilot.

La incorporación de PostgreSQL está prevista, pero
no debe darse por implementada hasta comprobarlo
en el código actual.

## 3. Arquitectura

El proyecto activo está formado por el backend en
backend/ y el frontend estático en frontend/.
La carpeta CarteraSoloHTML se considera un prototipo
legacy y no forma parte del desarrollo activo.

### Backend

- Aplicación basada en FastAPI.
- Punto de entrada: backend/app/main.py.
- API REST con rutas para autenticación, cartera,
  cotizaciones, liquidez, ahorro, operaciones y tickers.
- Organización por rutas, servicios, repositorios,
  esquemas y tareas de actualización.
- Los datos de ejemplo viven en backend/app/data/.
- Mantener separadas las rutas, la lógica de negocio
  y el acceso a datos.

### Frontend

- Aplicación web con HTML, CSS y JavaScript.
- Páginas principales: login.html, cartera.html y ahorro.html.
- Archivos compartidos en frontend/components/, frontend/css/
  y frontend/js/.
- Consume la API del backend mediante peticiones HTTP.
- Mantener separada la interfaz de la lógica de negocio.
- Evitar duplicar código JavaScript.

### Docker

- Utilizar Docker Compose para gestionar los servicios.
- Actualmente el servicio principal es backend con
  Uvicorn en el puerto 8000.
- Mantener configuraciones reproducibles.
- No introducir dependencias innecesarias.
- Revisar puertos, volúmenes y variables de entorno
  antes de modificar la configuración.

## 4. Instrucciones de desarrollo

- Antes de modificar archivos, inspeccionar el código
  existente y comprender su funcionamiento.
- Respetar la arquitectura y las convenciones actuales.
- Evitar reescribir componentes que ya funcionan.
- Proponer cambios pequeños y progresivos.
- No introducir librerías nuevas sin justificar
  su necesidad.
- No inventar endpoints, funciones ni estructuras
  que no existan en el proyecto.
- Si falta información, preguntar antes de asumir.
- Explicar brevemente los cambios realizados.

## 5. Python y FastAPI

- Utilizar código claro, legible y modular.
- Preferir funciones pequeñas con responsabilidades
  bien definidas.
- Utilizar anotaciones de tipos cuando aporten claridad.
- Gestionar correctamente las excepciones.
- Validar los datos recibidos por la API.
- Utilizar los mecanismos de validación de FastAPI
  y Pydantic cuando corresponda.
- Mantener la lógica de negocio fuera de las rutas
  cuando la complejidad lo justifique.

## 6. Frontend

- Mantener compatibilidad con los navegadores modernos.
- Utilizar JavaScript estándar salvo que exista
  una razón para añadir un framework.
- Gestionar los errores de las peticiones a la API.
- No almacenar contraseñas ni secretos en el frontend.
- Mantener una interfaz sencilla y coherente.

## 7. Seguridad

- No incluir contraseñas, tokens ni claves API
  directamente en el código.
- Utilizar variables de entorno para los secretos.
- Validar y sanear las entradas del usuario.
- No exponer información sensible en los logs.
- Revisar CORS y autenticación antes de desplegar
  la aplicación en producción.

## 8. Pruebas y validación

- Añadir pruebas cuando se incorporen funcionalidades.
- Ejecutar las pruebas existentes después de modificar
  el código.
- Comprobar que los endpoints responden correctamente.
- Verificar que los servicios Docker arrancan
  correctamente cuando se modifica su configuración.
- No afirmar que una prueba ha pasado si no se ha
  ejecutado realmente.

## 9. Forma de trabajar del asistente

- Responder en español.
- Ser conciso y explicar los pasos de forma ordenada.
- Priorizar soluciones sencillas y comprensibles.
- Para cambios importantes, dividir el trabajo
  en pasos pequeños.
- Antes de realizar modificaciones amplias,
  presentar un resumen del enfoque.
- Mostrar los archivos afectados y explicar
  qué se ha cambiado.
- No modificar archivos ajenos a la tarea solicitada.

## 10. Estado del proyecto

Este apartado debe mantenerse actualizado.

Antes de proponer cambios, revisar el estado real
del repositorio, los archivos y la configuración.

El desarrollo activo se centra en la estructura de
backend/ y frontend/. La carpeta CarteraSoloHTML
es un proyecto antiguo o de prueba, no un módulo
activo del sistema principal.

No asumir que las funcionalidades descritas en
la documentación ya están implementadas.