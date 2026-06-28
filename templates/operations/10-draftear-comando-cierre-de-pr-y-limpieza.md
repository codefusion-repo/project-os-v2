# Draftear Comando Cierre de PR y Limpieza

## Objetivo de la Operación
Ayudar al PM humano a cerrar un issue y su PR asociado a través de comandos de terminal sin fricción.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Scope del issue, diff del PR, salida de validación y estado vivo del PR/Issue en GitHub.
- **Qué compara/decide**: Determina, según el estado vivo, qué piezas del paquete de cierre faltan.
- **Qué entrega (Output)**: El PM command bundle común de cierre, que según el estado actual incluye:
  - comandos de comentario para piezas faltantes (REVIEW_RESULT / EXECUTION_REPORT / CORRECTION_REPORT / PM_DECISION / CLOSURE_COMMENT) cuando apliquen;
  - comando de mark-ready si el PR no está listo para review;
  - comando de merge si el PR no está merged;
  - comando de cierre del issue si el issue no está cerrado;
  - limpieza de la rama remota del issue si existe;
  - limpieza local siempre.
- **Qué NO debe hacer (Límites)**: Solo draftea el paquete de cierre; no ejecuta merge/close/cleanup. El browser chat draftea; el terminal agent no participa automáticamente; el Humano PM ejecuta el bundle.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (draftea el bundle). Humano PM (ejecuta).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.review_before_close`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.pm_command_bundle`
- **Evidence Required**: `evidence.issue_scope, evidence.pr_diff, evidence.validation_output`

## Variables PM
- **Requeridas**: `PR_NUMBER, ISSUE_NUMBER`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Estado de mergeabilidad y de cierre. `evidence.closure_evidence` es evidencia verificada o producida tras el cierre, no un sustituto de los requisitos de review-before-close.

## Placeholders PM (para templates de uso manual)
- <PR_NUMBER> <ISSUE_NUMBER>

## Ejemplo de Invocación
```
10-draftear-comando-cierre-de-pr-y-limpieza.md
PR_NUMBER=VALOR_AQUI ISSUE_NUMBER=VALOR_AQUI
```
