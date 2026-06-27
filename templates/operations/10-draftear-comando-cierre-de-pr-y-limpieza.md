# Draftear Comando Cierre de PR y Limpieza

## Objetivo de la Operación
Ayudar al PM humano a cerrar un issue y su PR asociado a través de comandos de terminal sin fricción.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Estado final del PR y del Issue.
- **Qué compara/decide**: Confirma que el PR ha sido aprobado o merged.
- **Qué entrega (Output)**: PM command bundle con `gh pr merge`, `gh issue close`, limpieza de branches locales/remotos.
- **Qué NO debe hacer (Límites)**: Ningún agente debe ejecutar este comando automáticamente. Es exclusivo para el humano PM.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (draftea el bundle). Humano PM (ejecuta).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.review_before_close`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.pm_command_bundle`
- **Evidence Required**: `evidence.closure_evidence`

## Variables PM
- **Requeridas**: `PR_NUMBER, ISSUE_NUMBER`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Estado de mergeabilidad

## Placeholders PM (para templates de uso manual)
- <PR_NUMBER> <ISSUE_NUMBER>

## Ejemplo de Invocación
```
10-draftear-comando-cierre-de-pr-y-limpieza.md
PR_NUMBER=VALOR_AQUI ISSUE_NUMBER=VALOR_AQUI
```
