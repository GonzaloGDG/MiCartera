# Especificación funcional: registro de operaciones de compra, venta y dividendo

## Estado
- Estado: `accepted`
- [x] Requisito definido
- [x] Especificación documentada
- [x] Diseño descrito
- [x] Implementación completada
- [x] Validado por el asistente
- [x] Revisado por el usuario
- [x] Especificación marcada como accepted

## 1. Contexto y objetivo
- Qué problema resuelve esta funcionalidad: permitir registrar movimientos financieros en la cartera y reflejarlos en `backend/app/data/operaciones.json`, modificando la liquidez del usuario según el tipo de operación.
- En qué parte del sistema afecta:
  - Backend: `backend/app/routes/operaciones.py`, `backend/app/services/operaciones_service.py`, `backend/app/schemas/operaciones.py`, `backend/app/repositories/operaciones_repository.py`
  - Frontend: formularios o modales de operaciones dentro de la cartera o flujo de movimientos, y la vista resumen de operaciones con misma apariencia visual que `frontend/ahorro.html`
  - Datos: `backend/app/data/operaciones.json`, `backend/app/data/tickers.json`
- Usuario o caso de uso principal: un usuario quiere registrar una compra, una venta o un dividendo asociado a una acción que ya tiene en cartera y consultar el resumen anual con el mismo estilo de ahorro.

## 2. Requisito
- Objetivo del cambio: permitir crear operaciones con los campos necesarios y validaciones específicas por tipo, que éstas se guarden en `operaciones.json` con `usuario` e `id` calculados automáticamente y que la vista tenga el mismo estilo visual que la pantalla de ahorro, con un resumen anual de las inversiones.
- Alcance previsto:
  - registro de operaciones de compra
  - registro de operaciones de venta
  - registro de operaciones de dividendo
  - validación de ticker, fecha, títulos, precio, comisión y moneda
  - actualización de liquidez del usuario según el tipo de movimiento
  - resumen visual de `Total invertido` y de los últimos 6 años con el importe invertido por año
  - cálculo del porcentaje respecto al año anterior para cada año
- Alcance no incluido:
  - cambios en la lógica FIFO de cartera no previstos por esta funcionalidad
  - nuevas pantallas de gestión de operaciones fuera del flujo actual
- Restricciones conocidas:
  - no inventar una nueva fuente de datos ni una base de datos distinta
  - respetar la estructura actual de archivos JSON del proyecto
  - mantener la compatibilidad con la validación actual de tickers
  - no romper el flujo de liquidez ni la lógica de compra/venta existente
  - cada operación actualiza la liquidez de su misma moneda, sin conversión entre divisas
  - el total invertido y los resúmenes anuales incluyen únicamente compras en EUR, al no existir aún conversión para operaciones

## 3. Especificación funcional
### 3.1 Comportamiento esperado
- El usuario podrá seleccionar un ticker válido desde `tickers.json`.
- El tipo de operación podrá ser: `Compra`, `Venta` o `Dividendo`.
- La fecha tendrá valor por defecto con la fecha actual del sistema si no se indica.
- Los títulos, precio y comisión deben respetar las reglas de cada tipo.
- El usuario se toma automáticamente de la sesión y el identificador de la operación lo genera el backend.
- La operación se guarda en `backend/app/data/operaciones.json` con la estructura estándar del proyecto.
- Si se produce un error o se registra una operación incorrecta, el usuario podrá borrarla y la liquidez se revertirá automáticamente según el tipo de movimiento.
- La pantalla de operaciones debe seguir la misma apariencia visual que `frontend/ahorro.html`: tarjetas de resumen, orden visual, estilos y tabla equivalente, sin cambiar la estructura general de la interfaz.
- Debe mostrarse una tarjeta con el `Total invertido` en la parte superior, seguida de los últimos 6 años con el importe invertido y el porcentaje respecto al año anterior.
- El cálculo del porcentaje debe seguir la regla: si el año anterior fue 1000 y el actual 1500, el incremento es `50%`.

### 3.2 Reglas de negocio
- El resumen anual debe basarse en el total invertido por año, calculado a partir de las operaciones registradas en `operaciones.json`.
- El cálculo del porcentaje por año debe compararse con el año inmediatamente anterior, usando la diferencia relativa sobre la base previa.
- Si el año anterior es 0, se interpretará como `0%` para evitar divisiones por cero o valores erróneos.
- Compra:
  - todos los campos son obligatorios
  - `titulos` debe ser mayor que 0
  - `precio` debe ser mayor o igual que 0
  - si `precio == 0`, se mostrará un popup de confirmación para avisar de posibilidad de dividendo en acciones
  - `comision` puede ser 0
  - la operación reduce la liquidez disponible del usuario
- Venta:
  - todos los campos son obligatorios
  - `titulos` debe ser mayor que 0
  - `precio` debe ser mayor que 0
  - `comision` puede ser 0
  - el número de títulos a vender no puede exceder los disponibles del usuario para ese ticker
  - la operación aumenta la liquidez del usuario
- Dividendo:
  - el ticker debe pertenecer a una posición que el usuario tenga en cartera
  - `titulos` serán los títulos que tiene el usuario para ese ticker
  - `precio` representa el dividendo bruto por acción
  - `comision` puede ser 0
  - la operación aumenta la liquidez disponible del usuario
- Borrado:
  - cualquier operación puede borrarse si corresponde a la última operación del ticker para ese usuario
  - al borrar una operación, la liquidez debe ajustarse en sentido inverso al impacto original
  - una compra eliminada devuelve el importe a la liquidez, y una venta o dividendo eliminado lo resta
- Común:
  - `moneda` tiene valor por defecto `EUR`
  - `usuario` se obtiene de la sesión iniciada; no se solicita en el formulario
  - `id` se genera automáticamente en backend y es único en el fichero de operaciones
  - la liquidez se modifica en la cuenta de la misma moneda que la operación
  - el total invertido y los resúmenes anuales suman el importe de las compras en EUR (`titulos * precio + comisión`); las operaciones en otras monedas quedan fuera de esos resúmenes hasta que haya conversión disponible

### 3.3 Datos de entrada y salida
#### Entrada
- Endpoints implicados: `GET /api/operaciones?usuario=<usuario>`, `GET /api/tickers`, `POST /api/operaciones` y `DELETE /api/operaciones/{id}?usuario=<usuario>`.
- Campos esperados:
  - `usuario`
  - `tipo` (`compra`, `venta`, `dividendo`)
  - `ticker`
  - `fecha`
  - `titulos`
  - `precio`
  - `comision`
  - `moneda`
- Estructura de ejemplo:

```json
{
  "usuario": "admin",
  "tipo": "compra",
  "ticker": "ANA.MC",
  "fecha": "2026-10-12",
  "titulos": 10,
  "precio": 120.5,
  "comision": 2.5,
  "moneda": "EUR"
}
```

#### Salida
- Respuesta esperada del backend al crear: objeto con `ok` y `datos` con la operación creada. El listado añade total invertido y seis totales anuales EUR.
- Estructura esperada en el JSON persistido:

```json
{
  "id": 99,
  "usuario": "admin",
  "tipo": "compra",
  "ticker": "ANA.MC",
  "fecha": "2026-10-12",
  "titulos": 10,
  "precio": 120.5,
  "comision": 2.5,
  "moneda": "EUR"
}
```
- Códigos de error esperados:
  - 400 por validación fallida
  - 400 si no hay liquidez suficiente para una compra
  - 400 si intenta vender más títulos de los disponibles
  - 400 si el ticker no existe o el dividendo no corresponde a una posición del usuario

## 4. Diseño técnico
### 4.1 Capas afectadas
- Backend:
  - `backend/app/routes/operaciones.py`
  - `backend/app/services/operaciones_service.py`
  - `backend/app/repositories/operaciones_repository.py`
  - `backend/app/schemas/operaciones.py`
- Frontend:
  - `frontend/operaciones.html`, accesible desde la navegación principal
  - `frontend/js/operaciones.js`
  - `frontend/css/operaciones.css`
  - formulario con selector de ticker, tipo, títulos, precio, comisión, fecha y moneda
  - flujo de validación de errores y confirmación en caso de precio 0 para compra
  - vista resumen con `Total invertido` y los últimos 6 años de inversión, siguiendo la misma apariencia visual que `frontend/ahorro.html`
- Datos:
  - `backend/app/data/operaciones.json`
  - `backend/app/data/tickers.json`
- Documentación:
  - README o docs si se documentan nuevas validaciones de negocio

### 4.2 Decisión de diseño
- La validación debe seguir siendo centralizada en el servicio, no duplicada en el frontend.
- La lógica de cómputo de liquidez debe reutilizar el servicio existente de liquidez para evitar inconsistencias.
- El tipo `dividendo` debe integrarse como un tipo más del sistema, con reglas específicas y sin romper la compatibilidad con `compra` y `venta`.
- La generación de `id` y `usuario` debe realizarse en la capa de repositorio/servicio y no depender del cliente.

### 4.3 Riesgos / dependencias
- Dependencias con otros módulos: liquidez, tickers, cartera FIFO y repositorio de operaciones.
- Compatibilidad con datos existentes: se debe mantener la estructura actual de `operaciones.json`.
- Impacto relevante: el cálculo de cartera, disponibilidad de títulos y saldo disponible se verá afectado por estas nuevas operaciones.

## 5. Historias / casos de uso
### Caso 1: compra válida
- El usuario selecciona un ticker válido, el tipo compra, fecha actual, 10 títulos, precio 120.5 y comisión 2.5.
- Resultado esperado: se crea la operación, se guarda con `id` y `usuario` automáticos y se descuenta del saldo disponible.

### Caso 2: venta válida
- El usuario tiene 20 acciones de un ticker y vende 5.
- Resultado esperado: se guarda la operación y se incrementa la liquidez disponible por la venta neta.

### Caso 3: compra con precio 0
- El usuario intenta crear una compra con `precio = 0`.
- Resultado esperado: se muestra un popup de confirmación indicando posibilidad de dividendo en acciones y la operación solo debe aceptarse si el usuario confirma.

### Caso 4: dividendo válido
- El usuario tiene títulos de `BBVA.MC` y registra un dividendo con ese ticker, titulos igual al número de acciones que posee, precio equivalente al dividendo bruto por acción y comisión 0.
- Resultado esperado: se registra la operación y se incrementa la liquidez por el importe calculado.

### Caso 5: borrado de operación incorrecta
- El usuario registra una operación por error y la borra desde la lista.
- Resultado esperado: la operación desaparece de `operaciones.json` y la liquidez del usuario vuelve al valor anterior al movimiento.

### Caso 6: caso límite
- El usuario intenta vender más títulos de los que tiene.
- Resultado esperado: error 400 con mensaje claro indicando los títulos disponibles.

## 6. Tareas de implementación
1. [x] Revisar la estructura actual de `operaciones.json` y `tickers.json`
2. [x] Extender el schema de operaciones para incluir `dividendo` y reglas de validación
3. [x] Implementar la validación de compra/venta/dividendo en el servicio
4. [x] Ajustar la lógica de actualización de liquidez para cada tipo y moneda
5. [x] Mantener la generación de `usuario` desde sesión y `id` en backend
6. [x] Añadir el borrado de operación con reversión de liquidez
7. [x] Implementar la interfaz de operaciones y la navegación
8. [x] Ejecutar pruebas relevantes de regresión
9. [x] Alinear el selector de ticker con la lista devuelta por `GET /api/tickers` y añadir una prueba de regresión

## 7. Plan de validación
### Backend
- Comando exacto: `cd backend && . .venv/bin/activate && python -m pytest -q app/tests`
- Resultado esperado: todas las pruebas de regresión del backend siguen pasando y las nuevas validaciones de operaciones no provocan errores.
- Casos de regresión: creación y borrado por API, compra, venta, dividendo, validación de títulos disponibles y liquidez.

### Frontend
- Comando exacto: `cd frontend && npm test`
- Resultado esperado: el flujo de creación de operaciones funciona sin errores y muestra los mensajes de validación esperados.
- La prueba E2E usa el formato real de `GET /api/tickers` (lista de objetos) y comprueba que se envía el símbolo del ticker, no el índice de la lista.
- La suite E2E comprueba la compra a precio cero con confirmación, el selector de ticker y títulos del dividendo, la selección de ticker para venta y el borrado de la última operación.

### Validación manual
- Probar una compra válida con comisión 0 y fecha actual.
- Probar una venta con títulos disponibles suficientes.
- Probar un dividendo de un ticker que exista en cartera.
- Comprobar que el popup aparece en compra con precio 0.
- Revisar que `operaciones.json` guarda cada operación con `usuario` e `id` generados automáticamente.

## 8. Criterios de aceptación
- [x] El usuario puede crear operaciones de compra, venta y dividendo desde el flujo definido
- [x] El backend valida correctamente cada tipo de operación
- [x] Los tickers se validan contra `tickers.json`
- [x] El usuario y el `id` se generan automáticamente desde la sesión/backend
- [x] La liquidez se actualiza según el tipo de operación y su moneda
- [x] La compra con precio 0 exige confirmación explícita
- [x] El dividendo valida que el ticker pertenece al usuario y que los títulos coinciden
- [x] El borrado de una operación revierte la liquidez al valor anterior
- [x] La vista de operaciones mantiene la misma estética que `ahorro.html`, con `Total invertido` y los últimos 6 años de inversión
- [x] El porcentaje anual se calcula respecto al año anterior, por ejemplo 1000 -> 1500 = 50%
- [x] Las pruebas relevantes pasan sin regresiones
- [x] La interfaz se revisó manualmente en navegador
