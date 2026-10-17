---
name: sdd-workflow
description: 'SDD workflow for MiCartera. Use when planning a feature, bug fix, or change request. Covers requirement, specification, design, task breakdown, and validation tests.'
argument-hint: 'Describe the feature/bug and the context (backend, frontend, API, UI, etc.).'
user-invocable: true
disable-model-invocation: false
---

# SDD workflow para MiCartera

## Quick start

Usa esta skill para definir, revisar y validar una funcionalidad antes de implementarla.

Cuando la uses, sigue este flujo básico:
1. Requisito: qué problema hay y qué se quiere lograr.
2. Especificación: qué debe hacer y bajo qué reglas.
3. Diseño: qué capas y archivos cambian.
4. Tareas: desglosa la ejecución en pasos verificables.
5. Validación: define pruebas y criterios de aceptación.

Es útil para:
- nuevas features
- correcciones de bugs
- cambios de API
- mejoras de frontend
- refactorizaciones con impacto funcional
- tareas con varios pasos y validación

## Objetivo

Convertir una idea o problema en una propuesta ejecutable, con:

1. requisito claro
2. especificación funcional
3. diseño técnico
4. tareas concretas
5. pruebas de validación

Esto mantiene el trabajo alineado con la arquitectura del proyecto y reduce ambigüedad antes de tocar código.

## Flujo recomendado

### 1) Requisito

Documenta el problema o necesidad en lenguaje claro.

Incluye:
- objetivo de negocio o técnico
- contexto del problema
- usuarios o módulos afectados
- restricciones conocidas
- alcance esperado

Formato mínimo:

```md
## Requisito
- Objetivo:
- Problema:
- Alcance:
- Restricciones:
```

### 2) Especificación

Define qué debe hacer la funcionalidad y cómo se comporta en escenarios normales y límite.

Incluye:
- entradas esperadas
- salidas esperadas
- reglas de negocio
- casos de éxito
- casos de error
- casos límite

Formato mínimo:

```md
## Especificación
### Comportamiento esperado
### Reglas
### Casos de éxito
### Casos de error
### Casos límite
```

### 3) Diseño

Explica la solución propuesta sin entrar en implementación de detalle, pero sí con suficiente claridad para decidir los archivos y capas implicadas.

Pregunta: ¿qué cambia en backend, frontend, datos, rutas, servicios, repositorios, componentes o tests?

Formato mínimo:

```md
## Diseño
### Capas afectadas
- Backend:
- Frontend:
- Datos:
### Decisiones principales
### Riesgos / dependencias
```

### 4) Tareas

Desglosa la implementación en pasos pequeños y verificables.

Cada tarea debe estar enfocada y ser ejecutable por una persona o por la IA sin ambigüedad.

Formato mínimo:

```md
## Tareas
1. [ ] Definir modelo o endpoint necesario
2. [ ] Implementar lógica en backend
3. [ ] Ajustar frontend si aplica
4. [ ] Ejecutar pruebas relevantes
5. [ ] Revisar resultado y documentar
```

### 5) Tests

Define la validación antes de implementar.

Incluye:
- pruebas unitarias o de integración relevantes
- pruebas end-to-end si afectan UI
- casos de regresión
- comando exacto a ejecutar

Formato mínimo:

```md
## Tests
- Backend: `python -m pytest -q app/tests/...`
- Frontend: `npm test`
- Validaciones manuales:
```

## Salida esperada

Al terminar el trabajo, la tarea debería quedar documentada con estas secciones:

- Requisito
- Especificación
- Diseño
- Tareas
- Test plan
- Criterios de aceptación

## Estado de trabajo en la especificación

La especificación debe llevar un bloque de estado con valores limitados y checkboxs (`[ ]` / `[x]`) para reflejar el estado real del cambio.

Estado permitido:
- `draft`
- `in_progress`
- `implemented`
- `accepted`

Regla recomendada:
- El asistente marca como completadas las tareas que ya ha ejecutado y validado con evidencia.
- El usuario marca como revisadas o aceptadas las tareas finales que ha comprobado en la práctica.
- Cuando la revisión manual del usuario está completa, se marca la especificación como `accepted`.

Ejemplo:

```md
## Estado
- Estado: `in_progress`
- [x] Definido el problema y el alcance
- [x] Especificado el comportamiento esperado
- [x] Diseñado la solución
- [x] Implementado el cambio
- [ ] Validado en navegador por el usuario
- [ ] Marcado como accepted tras revisión final
```

Esto permite distinguir claramente entre:
- trabajo ya ejecutado
- validación pendiente del usuario
- cierre final de la especificación

## Plantilla base

Puedes reutilizar la plantilla incluida en [assets/spec-template.md](./assets/spec-template.md).

## Principios del proyecto

- Mantener la arquitectura actual: backend, frontend, datos y documentación por separado.
- No inventar endpoints o estructuras sin necesidad.
- Reducir el alcance al mínimo viable.
- Validar con pruebas reales antes de cerrar la tarea.
- Preferir cambios pequeños, observables y reversibles.

## Regla de oro

Antes de escribir código, hay que dejar claro:

- qué se quiere,
- cómo debe comportarse,
- qué cambios serán necesarios,
- cómo se va a validar.

Si eso no existe, la tarea no está lista para implementarse.
