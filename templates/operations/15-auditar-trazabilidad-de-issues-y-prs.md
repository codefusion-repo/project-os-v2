# Auditar Trazabilidad de Issues y PRs

## Objetivo de la Operación
Verificar la existencia de evidencia de cierre (closure evidence) y trazabilidad completa de los issues para mantener el sistema de memoria basado en GitHub estable.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Historial de comentarios, labels, commits de un ISSUE_NUMBER.
- **Qué compara/decide**: La realidad del issue vs protocolo de trazabilidad de Project OS.
- **Qué entrega (Output)**: Reporte de vacíos: si falta PM decision, si no hay execution report, etc.
- **Qué NO debe hacer (Límites)**: No re-escribe comentarios pasados ni edita historial.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (revisión de trazabilidad PM-facing). Secundaria: `terminal_agent` (solo cuando se requiere correr el auditor local read-only sobre GitHub).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.review_only`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.status_result`
- **Evidence Required**: `evidence.repo_state`

## Variables PM
- **Requeridas**: `ISSUE_NUMBER`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Metadata de trazabilidad

## Placeholders PM (para templates de uso manual)
- <ISSUE_NUMBER>

## Ejemplo de Invocación
```
15-auditar-trazabilidad-de-issues-y-prs.md
ISSUE_NUMBER=VALOR_AQUI
```
