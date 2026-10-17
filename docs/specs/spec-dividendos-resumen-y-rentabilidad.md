# Especificación funcional: resumen y rentabilidad de dividendos

## Estado
- Estado: `draft`
- [x] Requisito definido
- [x] Especificación documentada
- [x] Diseño descrito
- [ ] Implementación completada
- [ ] Validado por el asistente
- [ ] Revisado por el usuario
- [ ] Especificación marcada como accepted

## 1. Contexto y objetivo
- Qué problema resuelve esta funcionalidad: sustituir la página provisional de dividendos por un resumen de los dividendos del usuario, su evolución anual y el rendimiento respecto al coste de adquisición de sus posiciones.
- En qué parte del sistema afecta:
  - Backend: ruta y servicio de dividendos; lectura de operaciones, tickers y coste de posiciones FIFO.
  - Frontend: `frontend/dividendos.html`, nueva lógica JavaScript y estilos coherentes con `frontend/cartera.html`.
  - Datos: `backend/app/data/operaciones.json` y `backend/app/data/tickers.json`.
- Usuario o caso de uso principal: el usuario consulta cuánto ha cobrado en dividendos, cómo ha variado por año y qué proporción representan frente al coste de compra de las acciones.

## 2. Requisito
- Objetivo del cambio: mostrar los dividendos calculados desde las operaciones del usuario, con vistas bruta y neta, importes anuales y un resumen por compañía.
- Alcance previsto:
  - Reemplazar el contenido provisional de `dividendos.html`.
  - Mostrar el total de dividendos cobrados y los últimos seis años naturales, incluyendo el actual.
  - Mostrar la variación porcentual anual frente al año natural anterior.
  - Mostrar una tabla por ticker con descripción, dividendos cobrados, moneda y rendimiento frente al coste total de adquisición.
  - Añadir un control global `Bruto` / `Neto`.
  - Crear en backend funciones aisladas para calcular el neto y convertir importes a EUR, inicialmente con factores fijos.
- Alcance no incluido:
  - Obtener retenciones reales por país, empresa o tipo de dividendo.
  - Consultar tipos de cambio reales o históricos.
  - Cambiar operaciones existentes o registrar pagos de dividendos nuevos.
- Restricciones conocidas:
  - La fuente de operaciones es `operaciones.json`; solo se suman registros del usuario solicitado cuyo tipo sea `dividendo`.
  - El importe bruto de cada pago es `titulos * precio`; la comisión no forma parte del cálculo especificado.
  - La divisa de la tabla por compañía se toma de `moneda` de las operaciones.
  - Los resúmenes generales se expresan en EUR. Los importes por compañía se mantienen en su moneda de origen; se convierten a EUR para cálculos globales.
  - Las funciones de neto y conversión deben vivir en backend para facilitar sustituir los factores fijos en el futuro.

## 3. Especificación funcional
### 3.1 Comportamiento esperado
- Al entrar en la página, el frontend consulta al backend usando el usuario de la sesión.
- La página mantiene la apariencia general de `cartera.html`: tarjetas de resumen en la cabecera, tipografía, colores, tabla y composición visual coherentes con sus estilos compartidos.
- En la cabecera se muestra:
  - Total de dividendos cobrados.
  - Una tarjeta para cada uno de los últimos seis años naturales, con el dividendo total y el porcentaje respecto al año anterior.
- La tabla muestra una fila por ticker y moneda, con:
  - ticker
  - descripción obtenida de `tickers.json`
  - importe total de dividendos cobrados en esa moneda
  - moneda de origen
  - porcentaje de dividendos cobrados respecto al coste total de adquisición de las acciones
- El control `Bruto` / `Neto` actualiza todos los importes de dividendos, totales anuales y porcentajes de la página sin cambiar la moneda de origen mostrada en la tabla.
- La vista se carga inicialmente en modo `Bruto`.
- Los cambios de modo se solicitan al backend; el factor neto no se calcula ni se hardcodea en el frontend.

### 3.2 Reglas de negocio
- Dividendo bruto por operación: `titulos * precio`.
- Modo `Bruto`: mostrar los importes calculados sin aplicar retención.
- Modo `Neto`: calcular en backend `bruto * 0.81`.
- Conversión a EUR en backend:
  - EUR permanece sin cambios.
  - Cualquier otra moneda se convierte multiplicando el importe por `1.11`.
  - El factor se aplica a importes generales y anuales usados para totalizar en EUR.
- Total general: suma en EUR de los dividendos del usuario, en el modo seleccionado.
- Total anual: suma en EUR de dividendos cuya fecha corresponde a ese año natural, en el modo seleccionado. Se muestran los seis últimos años naturales, incluyendo el año actual; los años sin dividendos se muestran con total cero.
- Variación anual: `((total_del_año - total_del_año_anterior) / total_del_año_anterior) * 100`, usando importes EUR en el modo seleccionado.
  - Si el año anterior no tiene importe positivo, mostrar `—` para no dividir entre cero.
  - Para el primero de los seis años, se compara con el año natural inmediatamente anterior aunque ese año no aparezca entre las seis tarjetas.
- Tabla por compañía:
  - El total de dividendos suma `titulos * precio` por usuario, ticker y moneda de origen.
  - Si un ticker tiene operaciones en más de una moneda, se muestra una fila separada por cada moneda para no sumar importes incompatibles.
  - El coste de adquisición se calcula con la misma lógica FIFO de posiciones abiertas que usa la cartera, incluyendo comisiones de compra y descontando las ventas.
  - El porcentaje es `dividendos cobrados / coste de adquisición * 100`. En modo neto, solo se aplica el factor `0.81` al importe de dividendos; el coste de adquisición no cambia.
  - Si no hay coste de adquisición positivo para el ticker, mostrar `—` como porcentaje.
- Los dividendos se totalizan usando la moneda registrada en cada operación; la conversión general a EUR usa el factor fijo indicado.
- Los campos ausentes o con valores no numéricos requeridos para los cálculos deben producir un error explícito de backend, no un total exitoso incompleto.
- Las operaciones con fecha no interpretable no pueden asignarse a un año: el backend debe excluirlas únicamente del resumen anual y señalar el problema explícitamente, sin descartar silenciosamente su importe del total general o de la tabla por compañía.

### 3.3 Datos de entrada y salida
#### Entrada
- Endpoint propuesto: `GET /api/dividendos?usuario=<usuario>&modo=bruto|neto`.
- `usuario` identifica las operaciones a consultar.
- `modo` acepta `bruto` o `neto`; si se omite, usa `bruto`.
- La fuente de dividendos es `operaciones.json`, filtrada por usuario y `tipo == "dividendo"`.
- Los nombres/descripciones y divisas de referencia de los tickers se consultan en `tickers.json`; la columna de divisa de la tabla corresponde a `moneda` de las operaciones.

#### Salida
- Respuesta JSON con `ok`, modo aplicado, moneda general (`EUR`), total general, resumen de los seis años y filas por ticker/moneda.
- Cada resumen anual incluye año, total en EUR y variación porcentual o `null` cuando no se puede calcular.
- Cada fila de compañía incluye ticker, descripción, total de dividendos en moneda de origen, moneda y porcentaje frente al coste de adquisición.
- La respuesta identifica operaciones con fechas no interpretables para poder informar al usuario de que no entraron en los totales anuales.
- Los errores de lectura o de datos inválidos se devuelven como error HTTP con un mensaje claro; no se responde con un resumen parcial como si fuera completo.

## 4. Diseño técnico
### 4.1 Capas afectadas
- Backend:
  - Nueva ruta `backend/app/routes/dividendos.py`, registrada en `backend/app/main.py`.
  - Nuevo servicio `backend/app/services/dividendos_service.py` para agregaciones, variación anual, rendimiento por compañía, cálculo neto y conversión fija a EUR.
  - Reutilizar `backend/app/repositories/operaciones_repository.py` para operaciones del usuario y `backend/app/repositories/tickers_repository.py` para descripciones.
  - Reutilizar la lógica de posiciones abiertas de `backend/app/services/fifo_service.py` para el coste de adquisición.
- Frontend:
  - Completar `frontend/dividendos.html`.
  - Añadir `frontend/js/dividendos.js`.
  - Añadir estilos específicos solo si no bastan los estilos compartidos de `frontend/css/cartera.css` y componentes comunes.
- Pruebas:
  - Pruebas unitarias/API para agregación, neto, conversión, año anterior cero, divisas múltiples, rendimiento FIFO y errores de datos.
  - Pruebas E2E para la pantalla, el cambio bruto/neto y la presentación de tarjetas y tabla.
- Datos:
  - Sin cambios al formato de `operaciones.json` ni de `tickers.json`.

### 4.2 Decisiones principales
- Mantener en backend los cálculos y factores financieros para que el frontend solo presente los resultados.
- Reutilizar los repositorios y el servicio FIFO existentes en lugar de duplicar acceso o cálculo de coste.
- Aplicar la retención al importe del dividendo, no al coste de adquisición.
- Mantener los importes de la tabla por compañía en la moneda registrada en las operaciones; convertir a EUR para el total general y las tarjetas anuales.
- Mantener aislados los factores `0.81` y `1.11` en funciones con responsabilidades claras, para que puedan sustituirse por cálculos reales más adelante.
- Mantener la respuesta y los controles de UI simples; la pantalla comienza en modo bruto y solicita el modo seleccionado al backend.

### 4.3 Riesgos / dependencias
- La lógica FIFO actual procesa compras y ventas; debe confirmarse que las operaciones de dividendo no alteran la cantidad ni el coste de las posiciones.
- La moneda guardada en cada operación debe ser coherente para comparar dividendos con su coste de adquisición. Si existe una mezcla de monedas en operaciones de un mismo ticker, el cálculo del porcentaje debe normalizar ambos importes a EUR antes de compararlos.
- Existen datos históricos de operaciones con fechas no interpretables; deben señalarse y excluirse solo de agregaciones anuales.
- El factor fijo `1.11` no representa un tipo de cambio real y debe identificarse como provisional en documentación o interfaz adecuada.

## 5. Historias / casos de uso
### Caso 1: consulta con datos válidos
- El usuario accede a Dividendos.
- Resultado esperado: ve el total general en EUR, las seis tarjetas anuales y las filas de compañía calculadas desde sus operaciones.

### Caso 2: alternar entre bruto y neto
- El usuario cambia de `Bruto` a `Neto`.
- Resultado esperado: el backend calcula dividendos con el factor `0.81`, actualiza importes y porcentajes de dividendos en toda la página y mantiene sin cambios el coste de adquisición.

### Caso 3: variación anual
- El usuario cobró 1000 EUR en dividendos en 2024 y 1500 EUR en 2025.
- Resultado esperado: el año 2025 muestra `50%` de variación frente a 2024.

### Caso 4: moneda extranjera
- El usuario registra 100 unidades de una moneda distinta de EUR.
- Resultado esperado: la fila de compañía muestra `100` en su moneda de origen y las agregaciones generales convierten ese importe a `111 EUR`.

### Caso 5: ticker sin coste abierto
- Hay operaciones de dividendo para un ticker sin posición abierta con coste de adquisición positivo.
- Resultado esperado: se muestra el total de dividendos y `—` para el porcentaje, sin error ni división por cero.

### Caso 6: año previo sin dividendos o fecha inválida
- No hubo cobros en el año anterior, o hay una operación de dividendo cuya fecha no se puede interpretar.
- Resultado esperado: la variación anual aparece como `—`; las fechas inválidas se informan y no se asignan a un año, sin perder sus importes del total general ni de la tabla.

## 6. Estado
- Estado: `draft`
- [x] Requisito definido
- [x] Especificación documentada
- [x] Diseño descrito
- [ ] Implementación completada
- [ ] Validado por el asistente
- [ ] Revisado por el usuario
- [ ] Especificación marcada como accepted

## 7. Tareas de implementación
1. [ ] Confirmar contrato de respuesta y comportamiento para datos históricos con fecha no interpretable.
2. [ ] Crear servicio con filtros por usuario, ticker/moneda, cálculos anual y total, rendimiento FIFO y funciones de neto/conversión a EUR.
3. [ ] Exponer el resumen con la ruta de dividendos y validar el modo `bruto`/`neto`.
4. [ ] Completar la interfaz siguiendo la apariencia de `cartera.html`.
5. [ ] Implementar tarjetas de seis años, tabla por ticker/moneda y control Neto/Bruto que actualiza toda la página.
6. [ ] Añadir pruebas unitarias/API para reglas de cálculo y errores/casos límite.
7. [ ] Añadir pruebas E2E para presentación y alternancia de modo.
8. [ ] Ejecutar las pruebas relevantes y revisar el resultado visual en navegador.

## 8. Plan de validación
### Backend
- Comando exacto: `cd backend && .venv/bin/python -m pytest -q app/tests`
- Resultado esperado: pruebas nuevas y existentes pasan; se verifican los cálculos EUR/nativo, neto/bruto, años, porcentaje anual, FIFO y datos inválidos.
- Casos de regresión: cartera FIFO, operaciones, usuario sin dividendos y operaciones de diferentes monedas.

### Frontend
- Comando exacto: `cd frontend && npm test`
- Resultado esperado: la página muestra el resumen y la tabla, permite alternar bruto/neto y presenta errores API de forma visible.

### Validación manual
- Comparar total general y tarjetas con operaciones de prueba conocidas.
- Confirmar el caso de 1000 EUR en 2024 y 1500 EUR en 2025 (variación de 50%).
- Confirmar que una moneda extranjera se mantiene en su unidad en la tabla y se convierte con `1.11` en los totales generales.
- Confirmar que el coste usado para el porcentaje coincide con la posición abierta FIFO de la cartera.
- Alternar Neto/Bruto y comprobar que cambian todos los importes de dividendos y sus porcentajes, pero no el coste de adquisición.

## 9. Criterios de aceptación
- [ ] Se muestra el total cobrado y el resumen de los últimos seis años, incluido el año actual.
- [ ] La variación anual compara cada año con el año natural anterior y muestra `—` si la base no es positiva.
- [ ] La tabla identifica ticker, descripción, importe por compañía, moneda de origen y porcentaje frente al coste FIFO.
- [ ] Las operaciones de dividendo se calculan como `titulos * precio`, sin sumar la comisión.
- [ ] El control bruto/neto aplica el factor neto en backend y actualiza todos los valores de dividendos de la página.
- [ ] Los totales generales y anuales se expresan en EUR mediante la función backend de conversión.
- [ ] Fechas inválidas y datos no numéricos se informan según las reglas especificadas y no se presentan como resultados completos silenciosamente.
- [ ] La interfaz sigue la apariencia general de `cartera.html` y las pruebas relevantes pasan sin regresiones.
