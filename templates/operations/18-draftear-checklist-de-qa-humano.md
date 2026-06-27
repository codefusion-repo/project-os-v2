# Draftear Checklist de QA Humano

## Objetivo de la Operación
Extraer los requerimientos no automatizables de un issue cerrado o en revisión, para un tercero (qa team, testing humano).

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Requisitos originales, aceptación de PM, cambios clave de UI/UX.
- **Qué compara/decide**: Mapea los technical changes contra flujos de uso humanos.
- **Qué entrega (Output)**: Lista Markdown lista para copiar o comentar en GitHub.
- **Qué NO debe hacer (Límites)**: El QA humano no es un actor de Project OS (no recibe route-prompts).

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (draftea). Destinatario: QA externo.**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.review_only`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.status_result`
- **Evidence Required**: `evidence.repo_state`

## Variables PM
- **Requeridas**: `ISSUE_NUMBER`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Testing instructions previas

## Placeholders PM (para templates de uso manual)
- <ISSUE_NUMBER>

## Ejemplo de Invocación
```
18-draftear-checklist-de-qa-humano.md
ISSUE_NUMBER=VALOR_AQUI
```
