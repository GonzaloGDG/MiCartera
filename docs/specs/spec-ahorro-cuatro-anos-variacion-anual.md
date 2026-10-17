# Especificación funcional: cuatro años y variación anual en Ahorro

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
- Qué problema resuelve esta funcionalidad: el resumen anual de la pantalla Ahorro muestra tres tarjetas y queda desequilibrado visualmente, además de no indicar la variación de un año a otro.
- En qué parte del sistema afecta:
  - Backend: agregación anual de movimientos en `backend/app/services/ahorro_service.py`.
  - Frontend: resumen de `frontend/ahorro.html` y renderizado en `frontend/js/ahorro.js`.
  - Estilos: `frontend/css/ahorro.css` y estilos compartidos si son necesarios.
- Usuario o caso de uso principal: el usuario consulta el total neto de ahorro y compara la evolución anual de sus aportaciones netas.

## 2. Requisito
- Objetivo del cambio: mostrar cuatro años consecutivos en el resumen anual de Ahorro y el porcentaje de variación de cada año respecto al año anterior.
- Alcance previsto:
  - Presentar cuatro tarjetas anuales en una cuadrícula equilibrada de dos columnas por dos filas en escritorio.
  - Incluir el año actual y los tres años naturales anteriores.
  - Mostrar en cada tarjeta el total neto del año y su porcentaje de variación respecto al año previo.
- Alcance no incluido:
  - Cambiar el cálculo del total neto histórico o los movimientos de ahorro.
  - Añadir gráficos o nuevos tipos de movimiento.
- Restricciones conocidas:
  - Mantener el estilo existente de la página Ahorro.
  - El total anual conserva la definición actual: ingresos menos retiradas.
  - En pantallas estrechas la cuadrícula puede adaptarse al ancho disponible, manteniendo legibilidad.

## 3. Especificación funcional
### 3.1 Comportamiento esperado
- Al cargar Ahorro, la sección de totales anuales muestra exactamente los últimos cuatro años naturales, incluido el año actual.
- Los años se muestran en orden cronológico y cada tarjeta muestra el total neto y la variación porcentual frente al año inmediatamente anterior.
- Si un año no tiene movimientos, su total se muestra como `0,00 €` y su variación como `—` cuando no exista una base anterior positiva.
- Las cuatro tarjetas se distribuyen como cuadrícula 2 × 2 en el diseño de escritorio.

### 3.2 Reglas de negocio
- El importe anual se calcula como suma de ingresos menos suma de retiradas del año, reutilizando la lógica actual de `totales_anuales`.
- La variación anual se calcula como:
  `((total_neto_año_actual - total_neto_año_anterior) / total_neto_año_anterior) * 100`.
- Si el total del año anterior es cero o negativo, se muestra `—` para evitar una comparación porcentual sin base válida.
- Para el primer año mostrado se consulta también el total del año natural anterior, aunque ese año no tenga tarjeta.
- Los porcentajes se redondean a dos decimales y se presentan con signo y símbolo `%`; un resultado positivo, por ejemplo de 1000 a 1500, se muestra como `+50,00 %`.
- Los años con total negativo conservan el estilo visual que corresponda al valor neto de la tarjeta.

### 3.3 Datos de entrada y salida
#### Entrada
- Endpoint actual: `GET /api/ahorro?usuario=<usuario>`.
- Datos: movimientos de ahorro del usuario con tipo, importe y fecha.

#### Salida
- La respuesta del backend aporta totales netos por año para los años necesarios para calcular las cuatro tarjetas y su comparación con el año previo más antiguo.
- Cada tarjeta presenta año, total neto y variación porcentual o `null`/sin valor cuando la base previa no sea positiva.
- No se necesita crear un endpoint nuevo.

## 4. Diseño técnico
### 4.1 Capas afectadas
- Backend:
  - `backend/app/services/ahorro_service.py`: proporcionar los totales anuales necesarios, incluidos años sin movimientos para la ventana mostrada.
  - `backend/app/tests/test_ahorro.py`: probar la selección temporal y las sumas anuales.
- Frontend:
  - `frontend/ahorro.html`: contenedor de las tarjetas anuales.
  - `frontend/js/ahorro.js`: selección de cuatro años y renderizado de variación.
  - `frontend/css/ahorro.css`: distribución visual de las cuatro tarjetas.
  - `frontend/tests/e2e/ahorro.spec.js`: comprobar número, orden y contenido de tarjetas.

### 4.2 Decisiones principales
- Calcular los totales netos anuales en backend, reutilizando los agregados existentes.
- Derivar la ventana de cuatro años a partir del año actual del sistema, no de los años que casualmente tengan movimientos, para que siempre haya cuatro tarjetas.
- Mantener la tarjeta de total neto histórico y la tarjeta de liquidez sin cambios.
- Hacer responsive la cuadrícula según el patrón de estilos existente.

### 4.3 Riesgos / dependencias
- La fecha del sistema determina qué cuatro años se muestran.
- La variación puede no estar definida cuando el año anterior no tuvo ahorro neto positivo; en ese caso se muestra `—`.
- Debe conservarse la compatibilidad con la respuesta y los tests actuales del endpoint de ahorro.

## 5. Historias / casos de uso
### Caso 1: año con crecimiento
- El total neto de 2024 es 1000 y el de 2025 es 1500.
- Resultado esperado: la tarjeta de 2025 muestra `+50,00 %` respecto a 2024.

### Caso 2: año sin movimientos
- Uno de los últimos cuatro años no tiene movimientos.
- Resultado esperado: se muestra la tarjeta del año con total `0,00 €`; la cuadrícula sigue teniendo cuatro tarjetas.

### Caso 3: año anterior sin base positiva
- El total neto del año anterior es cero o negativo.
- Resultado esperado: la tarjeta del año comparado muestra `—` en vez de un porcentaje.

## 6. Tareas de implementación
1. [ ] Ajustar la respuesta/agregación del ahorro para incluir los totales de los cuatro años y la base del año previo.
2. [ ] Renderizar cuatro tarjetas anuales con total neto y variación porcentual.
3. [ ] Ajustar la cuadrícula a dos columnas y dos filas en escritorio y conservar su adaptación responsive.
4. [ ] Añadir pruebas backend para años vacíos, importes netos y selección de años.
5. [ ] Añadir o actualizar pruebas E2E para cuatro tarjetas, orden y porcentaje.
6. [ ] Ejecutar pruebas relevantes y revisar visualmente la página.

## 7. Plan de validación
### Backend
- Comando exacto: `cd backend && .venv/bin/python -m pytest -q app/tests/test_ahorro.py`
- Resultado esperado: se devuelven los totales anuales esperados, incluyendo años sin movimientos en la ventana mostrada, sin alterar total histórico ni liquidez.

### Frontend
- Comando exacto: `cd frontend && npm test -- --grep ahorro`
- Resultado esperado: cuatro tarjetas aparecen en orden, muestran importes y variaciones correctos, y el diseño se distribuye en dos filas de dos tarjetas en escritorio.

### Validación manual
- Confirmar que siempre aparecen los cuatro años naturales más recientes, incluido el actual.
- Confirmar el ejemplo: 1000 en el año previo y 1500 en el actual da `+50,00 %`.
- Confirmar la presentación `—` si el año anterior no tuvo un total neto positivo.
- Comprobar que las tarjetas se ven equilibradas y responsive.

## 8. Criterios de aceptación
- [ ] La pantalla Ahorro muestra exactamente cuatro tarjetas de años consecutivos, incluido el actual.
- [ ] Las tarjetas quedan visualmente equilibradas en dos columnas y dos filas en escritorio.
- [ ] Cada tarjeta muestra el total neto anual y su variación porcentual frente al año anterior.
- [ ] La variación usa ingresos menos retiradas y muestra `—` si la base anterior no es positiva.
- [ ] No cambian el total neto histórico, la liquidez ni el registro de movimientos.
- [ ] Las pruebas relevantes pasan y no hay regresiones.
