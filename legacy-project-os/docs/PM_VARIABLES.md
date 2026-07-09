# PM Variables (Variables del PM)

Este documento explica el sistema de variables del PM usado en operaciones y plantillas. Las variables son **selectores de contexto y parámetros de entrada**, NO son fronteras de autorización.

## Sintaxis
- **Sintaxis de Placeholder**: `<NOMBRE_VARIABLE>` (ej. `<ISSUE_NUMBER>`)
- **Sintaxis de Invocación (Override)**: `NOMBRE_VARIABLE=VALOR` (ej. `ISSUE_NUMBER=<ISSUE_NUMBER>`)

## Reglas de Normalización y Conflictos
1. Solo como ejemplo de normalización: `ISSUE_NUMBER` y `PR_NUMBER` pueden escribirse como un número desnudo o con `#`; el texto humano/Markdown generado siempre los renderiza con el prefijo `#`.
2. Las variables explícitas dadas en el mensaje actual del PM tienen la prioridad más alta.
3. El estado de GitHub inferido se usa solo cuando falta la variable.
4. Si falta una variable requerida, se emite `status.needs_context` o `status.needs_pm_decision`.
5. Si las variables entran en conflicto con la realidad (ej. PR_NUMBER no existe), el sistema debe fallar cerradamente.
6. Tipos/nombres son canónicos: `PM_FEEDBACK_HUMANO` y `PM_QUESTION_HUMANO` son las variables humanas aceptadas. No se permiten variantes con errores de tipeo.

## Variables Humanas Canónicas
- `PM_FEEDBACK_HUMANO`: contexto, criterio o interpretación adicional del PM. Es opcional y nunca reemplaza evidencia viva requerida.
- `PM_QUESTION_HUMANO`: pregunta del PM para interpretación, ruteo, aclaración, priorización, roadmap, review o soporte de decisión. Es opcional y nunca otorga autorización.
- `PM_QUESTION` es inválida y fue removida. No existe como alias, compatibilidad legacy, fixture aceptado ni entrada tolerada.

## Reglas de Secret-Safety
Las variables **NUNCA** deben portar o exponer contraseñas, secretos, tokens, credenciales, variables `.env`, cookies, o strings que parezcan llaves privadas.
Toda información confidencial hallada debe redactarse como `[REDACTED]` reportando el tipo de riesgo.

## Autorización
`PM_AUTHORIZATION_STATUS` es especial. No se asume por defecto; debe pasarse explícitamente cuando un route-prompt asegura contar con la autorización del humano PM para trabajos de escritura. Sus únicos valores de autorización son `pending` y `granted for this exact scope and mode`; draft/read-only/planning describen modo o postura, no autorización.

## Ejemplos de Uso
- Invocando un análisis de PR: `templates/operations/09-review-pr-before-close-and-draft-package.md PR_NUMBER=<PR_NUMBER>`
- Rutear corrección: `templates/operations/08-draft-review-correction-route-prompt.md ISSUE_NUMBER=<ISSUE_NUMBER> PM_FEEDBACK_HUMANO="Por favor, ajusta los nombres de archivos."`
- Pregunta ad-hoc: `templates/operations/05-review-project-state-and-misalignment.md PM_QUESTION_HUMANO="¿Estamos listos para el tag v0.2.0?"`
