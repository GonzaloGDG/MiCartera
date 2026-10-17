# Especificación funcional: Liquidez en cartera muestra 0 aunque exista saldo

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
- Qué problema resuelve esta funcionalidad: corregir que la pantalla de cartera muestre el saldo real de liquidez y no un valor 0 cuando existe dinero en `backend/app/data/liquidez.json`.
- En qué parte del sistema afecta:
  - Backend: route `GET /liquidez` y servicio `obtener_liquidez`
  - Frontend: `frontend/js/cartera.js` y la pantalla `frontend/cartera.html`
- Usuario o caso de uso principal: el usuario entra en la cartera y espera ver el importe disponible actualizado usando el saldo real guardado en backend.

## 2. Requisito
- Objetivo del cambio: que la liquidez mostrada en la cartera se obtenga correctamente desde el backend usando el servicio y el dato real del archivo JSON.
- Alcance previsto: la carga de la cartera y el valor de liquidez asociado en la pantalla principal.
- Alcance no incluido: cambios funcionales en ahorro, movimientos o otras pantallas no relacionadas.
- Restricciones conocidas:
  - no debe inventarse una nueva fuente de datos
  - debe respetarse la estructura actual de la API
  - la corrección debe ser compatible con el flujo actual de sesión del usuario

## 3. Especificación funcional
### 3.1 Comportamiento esperado
- Cuando el usuario accede a `cartera.html`, la aplicación debe consultar la API de cartera y la API de liquidez usando el usuario actual.
- La respuesta de `/liquidez` debe incluir el importe total de liquidez disponible en el formato que espera el frontend.
- La pantalla de cartera debe renderizar ese valor en el resumen de liquidez y no mostrar 0 si el saldo existe en `liquidez.json`.

### 3.2 Reglas de negocio
- La liquidez debe calcularse desde los datos del usuario autenticado.
- Solo se deben considerar cuentas con moneda `EUR` para el total que se muestra en cartera.
- Si no hay saldo para el usuario, el valor debe ser 0 y no un error funcional.
- Si la API devuelve un formato incorrecto, la interfaz no debe asumir un valor por defecto erróneo.

### 3.3 Datos de entrada y salida
#### Entrada
- Endpoint o acción involucrada: `GET /liquidez?usuario=<usuario>`
- Estructura esperada del dato guardado en JSON:
  - usuario
  - moneda
  - importe

#### Salida
- Respuesta esperada del backend: un objeto con al menos `ok`, `total` y `moneda`, o bien un contrato equivalente compatible con el frontend.
- Estructura esperada por `frontend/js/cartera.js`:
  - `dataLiquidez.total`
  - y el valor final debe ser un número válido
- Códigos de error:
  - 200 con saldo correcto
  - 400 si el usuario no es válido o si el servicio informa un error de dominio

## 4. Diseño técnico
### 4.1 Capas afectadas
- Backend:
  - ruta `backend/app/routes/liquidez.py`
  - servicio `backend/app/services/liquidez_service.py`
  - repositorio `backend/app/repositories/liquidez_repository.py`
- Frontend:
  - `frontend/js/cartera.js`
  - `frontend/cartera.html`
- Datos:
  - `backend/app/data/liquidez.json`
- Documentación:
  - README o docs si se documenta el comportamiento de la API

### 4.2 Decisión de diseño
- La API de liquidez debe devolver la misma estructura que el frontend espera para evitar soluciones ad hoc en la vista.
- La lógica de cálculo del total debe seguir residiendo en el servicio, no duplicarse en el frontend.
- La pantalla de cartera debe consumir la respuesta del backend tal y como está definida, sin realizar cálculos manuales ambiguos.

### 4.3 Riesgos / dependencias
- Dependencias con otros módulos: cartera, ahorro y sesión del usuario.
- Compatibilidad con datos existentes: debe seguir funcionando con el JSON actual de liquidez.
- Impacto relevante: la compra/venta de activos y la cuenta de ahorro dependen del saldo real disponible.

## 5. Historias / casos de uso
### Caso 1: flujo correcto
- El usuario inicia sesión y accede a la cartera.
- El frontend llama a `/cartera` y `/liquidez` con el usuario actual.
- El backend devuelve el total correcto según `liquidez.json`.
- Resultado esperado: la pantalla muestra el valor real, por ejemplo 11656.29 € para el usuario `admin`.

### Caso 2: error en validación
- Si el backend devuelve un formato distinto, por ejemplo `importe: {...}` en lugar de `total`, el frontend debe interpretar el payload correcto o la API debe corregirse.
- Resultado esperado: no aparece 0 por defecto ni un valor incoherente.

### Caso 3: caso límite
- Si no existe ninguna cuenta EUR para el usuario, el servicio debe devolver 0 y la UI debe renderizar 0 € sin romper la pantalla.
- Resultado esperado: la página sigue funcionando y muestra 0 € en lugar de fallar.

## 6. Tareas de implementación
1. [x] Revisar la respuesta de `GET /liquidez` y confirmarla contra lo que espera `cartera.js`
2. [x] Ajustar la ruta o el servicio para devolver `total` y propiedades compatibles con la pantalla de cartera
3. [x] Validar que el valor sea calculado desde `liquidez.json` y la moneda EUR
4. [ ] Comprobar el flujo de carga de la cartera para que la UI renderice el valor correcto
5. [x] Ejecutar pruebas relevantes del backend y validar la pantalla en lógica

## 7. Plan de validación
### Backend
- Comando exacto: `cd backend && . .venv/bin/activate && python -m pytest -q app/tests`
- Resultado esperado: la batería de pruebas sigue pasando y las pruebas relacionadas con liquidez no regresan.
- Casos de regresión: validación del flujo autenticado, liquidez y cartera.

### Frontend
- Comando exacto: `cd frontend && npm test`
- Resultado esperado: la carga de la pantalla de cartera no muestra liquidez 0 cuando el backend responde datos válidos.

### Validación manual
- Abrir la pantalla de cartera con el usuario `admin`.
- Confirmar que el resumen de liquidez coincide con el importe del archivo `liquidez.json`.
- Verificar que la carga no falla al convertir un valor que no existe.

## 8. Criterios de aceptación
- [x] La API de liquidez devuelve el valor en el formato esperado por el frontend
- [x] La pantalla de cartera muestra el saldo real en lugar de 0
- [x] El cálculo sigue usando el servicio de liquidez y no duplica lógica en el cliente
- [x] Las pruebas relevantes pasan y no hay regresiones del flujo principal

### Estado de aceptación
- [x] Revisión manual de la pantalla de cartera en navegador
- [x] Confirmación del valor mostrado con la fuente real de datos
- [x] Cierre formal de la especificación como resuelta
