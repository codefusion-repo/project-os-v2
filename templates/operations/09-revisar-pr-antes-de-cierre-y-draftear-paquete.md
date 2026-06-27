# Revisar PR antes de Cierre y Draftear Paquete

## Objetivo de la Operación
Analizar la implementación en un PR comparándola contra el issue vinculado para asegurar aceptación, generar el resultado del review, y sugerir el comando de cierre si aplica.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: PR_NUMBER diff, archivos cambiados, issue original vinculado, criterios de aceptación.
- **Qué compara/decide**: Verifica scope, out-of-scope, reglas de secret-safety y que todo se cumplió.
- **Qué entrega (Output)**: Primero un `output.review_result` (verdict: resolved, correction_needed, etc.). Segundo, solo si resolved, un `output.closure_comment` o el bundle de cierre.
- **Qué NO debe hacer (Límites)**: No usa `evidence.review_evidence` ni `evidence.closure_evidence` como sustituto de leer el scope del issue, el diff del PR y la salida de validación. Debe inspeccionar `evidence.issue_scope`, `evidence.pr_diff` y `evidence.validation_output`.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` o `terminal_agent` (dependiendo de dónde se hace el review).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.review_before_close`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.review_result`
- **Evidence Required**: `evidence.issue_scope, evidence.pr_diff, evidence.validation_output`

## Variables PM
- **Requeridas**: `PR_NUMBER`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Commits y diff del PR

## Placeholders PM (para templates de uso manual)
- <PR_NUMBER>

## Ejemplo de Invocación
```
09-revisar-pr-antes-de-cierre-y-draftear-paquete.md
PR_NUMBER=VALOR_AQUI
```
