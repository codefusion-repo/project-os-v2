# Verificar Estado Post-Merge

## Objetivo de la Operación
Comprobar que tras el cierre de un PR, la rama principal quedó saludable y las referencias de issues se resolvieron correctamente en GitHub.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Main branch actual, issue status, GitHub actions.
- **Qué compara/decide**: Detecta si el merge causó quiebres, archivos no intencionados, o si el issue vinculado no se cerró.
- **Qué entrega (Output)**: Reporte de sanidad del repositorio (status_result).
- **Qué NO debe hacer (Límites)**: No arregla errores automáticamente, solo reporta.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` o `terminal_agent` (read-only verification).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.review_only`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.status_result`
- **Evidence Required**: `evidence.repo_state`

## Variables PM
- **Requeridas**: `PR_NUMBER`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Últimos commits en main

## Placeholders PM (para templates de uso manual)
- <PR_NUMBER>

## Ejemplo de Invocación
```
11-verificar-estado-post-merge.md
PR_NUMBER=VALOR_AQUI
```
