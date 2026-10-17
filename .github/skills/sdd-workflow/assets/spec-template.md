# Especificación funcional: [Nombre de la funcionalidad]

## 1. Contexto y objetivo
- Qué problema resuelve esta funcionalidad:
- En qué parte del sistema afecta:
  - Backend:
  - Frontend:
- Usuario o caso de uso principal:

## 2. Requisito
- Objetivo del cambio:
- Alcance previsto:
- Alcance no incluido:
- Restricciones conocidas:

## 3. Especificación funcional
### 3.1 Comportamiento esperado
- Qué debe ocurrir cuando el usuario o sistema hace X:
- Qué respuesta debe devolver la API:
- Qué elementos deben verse en la interfaz:

### 3.2 Reglas de negocio
- Validaciones obligatorias:
- Regla de cálculo o estado:
- Casos de error:
- Casos límite:

### 3.3 Datos de entrada y salida
#### Entrada
- Endpoint o acción involucrada:
- Estructura esperada:
- Campos obligatorios / opcionales:

#### Salida
- Respuesta esperada:
- Estructura de datos:
- Códigos de error:

## 4. Diseño técnico
### 4.1 Capas afectadas
- Backend:
  - rutas
  - servicios
  - repositorios
  - schemas
- Frontend:
  - página / JS / componentes
- Datos:
  - ficheros JSON o ejemplos usados
- Documentación:
  - README / docs si aplica

### 4.2 Decisión de diseño
- Qué capa se encarga de la validación:
- Dónde se calcula la lógica:
- Cómo se integrará con la API existente:

### 4.3 Riesgos / dependencias
- Dependencias con otros módulos:
- Compatibilidad con datos existentes:
- Impacto en cartera, ahorro, liquidez, operaciones, tickers, etc.:

## 5. Historias / casos de uso
### Caso 1: flujo correcto
- Paso a paso del usuario o llamada:
- Resultado esperado:

### Caso 2: error en validación
- Entrada inválida:
- Resultado esperado:

### Caso 3: caso límite
- Datos vacíos / inconsistente / no previsto:
- Resultado esperado:

## 6. Estado
- Estado: `draft`
- [ ] Requisito definido
- [ ] Especificación documentada
- [ ] Diseño descrito
- [ ] Implementación completada
- [ ] Validado por el asistente
- [ ] Revisado por el usuario
- [ ] Especificación marcada como accepted

## 7. Tareas de implementación
1. [ ] Revisar punto de entrada en backend/frontend
2. [ ] Definir schema o contrato de datos
3. [ ] Implementar lógica de negocio
4. [ ] Conectar con la capa relevante
5. [ ] Ajustar interfaz si aplica
6. [ ] Ejecutar pruebas

## 8. Plan de validación
### Backend
- Comando exacto:
- Resultado esperado:
- Casos de regresión:

### Frontend
- Comando exacto:
- Resultado esperado:

### Validación manual
- Qué comprobar en la UI:
- Qué comprobar en la API:

## 8. Criterios de aceptación
- [ ] La funcionalidad responde correctamente al caso principal
- [ ] Los errores se gestionan de forma clara
- [ ] La lógica no rompe otros flujos del proyecto
- [ ] Las pruebas relevantes pasan
