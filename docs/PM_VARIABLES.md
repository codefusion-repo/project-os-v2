# PM Variables (Variables del PM)

Este documento explica el sistema de variables del PM usado en operaciones y plantillas. Las variables son **selectores de contexto y parámetros de entrada**, NO son fronteras de autorización.

## Sintaxis
- **Sintaxis de Placeholder**: `<NOMBRE_VARIABLE>` (ej. `<ISSUE_NUMBER>`)
- **Sintaxis de Invocación (Override)**: `NOMBRE_VARIABLE=VALOR` (ej. `ISSUE_NUMBER=123` o `ISSUE_NUMBER=#123`)

## Reglas de Normalización y Conflictos
1. `ISSUE_NUMBER` y `PR_NUMBER` aceptan tanto `123` como `#123`. En el texto humano/Markdown generado, siempre deben renderizarse como `#123`.
2. Las variables explícitas dadas en el mensaje actual del PM tienen la prioridad más alta.
3. El estado de Github inferido se usa solo cuando falta la variable.
4. Si falta una variable requerida, se emite `status.needs_context` o `status.needs_pm_decision`.
5. Si las variables entran en conflicto con la realidad (ej. PR_NUMBER no existe), el sistema debe fallar cerradamente.
6. Tipos/Nombres son canónicos: `FEEDBACK_PM_HUMANO` (No se permite usar PM_FEEDBACK_HUMANNO u otras variantes con errores de tipeo).

## Reglas de Secret-Safety
Las variables **NUNCA** deben portar o exponer contraseñas, secretos, tokens, credenciales, variables `.env`, cookies, o strings que parezcan llaves privadas.
Toda información confidencial hallada debe redactarse como `[REDACTED]` reportando el tipo de riesgo.

## Autorización
`PM_AUTHORIZATION_STATUS` es especial. No se asume por defecto; debe pasarse explícitamente cuando un route-prompt asegura contar con la autorización del humano PM para trabajos de escritura.

## Ejemplos de Uso
- Invocando un análisis de PR: `templates/operations/09-revisar-pr-antes-de-cierre-y-draftear-paquete.md PR_NUMBER=#456`
- Rutear corrección: `templates/operations/08-draftear-route-prompt-para-correcciones-de-review.md ISSUE_NUMBER=123 FEEDBACK_PM_HUMANO="Por favor, ajusta los nombres de archivos."`
- Pregunta ad-hoc: `templates/operations/05-revisar-estado-del-proyecto-y-desalineaciones.md PM_QUESTION="¿Estamos listos para el tag v0.2.0?"`
