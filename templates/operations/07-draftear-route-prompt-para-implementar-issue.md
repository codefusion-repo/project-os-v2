# Draftear Route-Prompt para Implementar Issue

## Objetivo de la Operación
Preparar un payload estructurado según `templates/route-prompt.md` para despachar trabajo de código a un terminal agent.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Issue #ISSUE_NUMBER, contexto del código, requerimientos.
- **Qué compara/decide**: Verifica si se requiere contexto extra antes de delegar la implementación.
- **Qué entrega (Output)**: Un route-prompt exacto que incluye PM_AUTHORIZATION_STATUS para que el agent lo ejecute.
- **Qué NO debe hacer (Límites)**: El browser chat NO ejecuta código. Solo prepara las instrucciones formales.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (draft). Secundaria: `terminal_agent` (ejecuta si es ruteado por el humano).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.pm_intake`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.route_prompt`
- **Evidence Required**: `evidence.source_basis, evidence.repo_state`

## Variables PM
- **Requeridas**: `ISSUE_NUMBER`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Estado del issue

## Placeholders PM (para templates de uso manual)
- <ISSUE_NUMBER>

## Ejemplo de Invocación
```
07-draftear-route-prompt-para-implementar-issue.md
ISSUE_NUMBER=VALOR_AQUI
```
