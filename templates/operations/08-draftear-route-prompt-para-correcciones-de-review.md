# Draftear Route-Prompt para Correcciones de Review

## Objetivo de la Operación
Encapsular feedback humano en un route-prompt para corregir un PR o branch específico sin expandir el scope.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Issue original, PR asociado, FEEDBACK_PM_HUMANO.
- **Qué compara/decide**: Alinea el feedback contra la implementación actual para focalizar la corrección.
- **Qué entrega (Output)**: Route-prompt de corrección (variante de corrección).
- **Qué NO debe hacer (Límites)**: No debe reimplementar el issue entero, ni expandir el scope de la tarea.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (draft). Secundaria: `terminal_agent` (ejecutor de corrección).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.pm_intake`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.route_prompt`
- **Evidence Required**: `evidence.repo_state`

## Variables PM
- **Requeridas**: `ISSUE_NUMBER, FEEDBACK_PM_HUMANO`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Archivos modificados por el PR

## Placeholders PM (para templates de uso manual)
- <ISSUE_NUMBER> <FEEDBACK_PM_HUMANO>

## Ejemplo de Invocación
```
08-draftear-route-prompt-para-correcciones-de-review.md
ISSUE_NUMBER=VALOR_AQUI FEEDBACK_PM_HUMANO=VALOR_AQUI
```
