# Revisar Estado del Proyecto y Desalineaciones

## Objetivo de la Operación
Tomar las decisiones del PM Humano y documentos fijos como fuente principal de la verdad, para encontrar desalineaciones con el código actual, roadmap o issues abiertos.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Decisiones PM, roadmap, issues abiertos y cerrados recientemente, código actual.
- **Qué compara/decide**: Detecta contradicciones entre la documentación/roadmap y la realidad viva de GitHub.
- **Qué entrega (Output)**: Reporte de hallazgos de alineación, y respuesta a PM_QUESTION usando live-state como contexto.
- **Qué NO debe hacer (Límites)**: No genera issues ni asume resoluciones; solo reporta.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (análisis PM-facing).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.review_only`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.status_result`
- **Evidence Required**: `evidence.repo_state`

## Variables PM
- **Requeridas**: `Ninguna`
- **Opcionales**: `PM_QUESTION`
- **Inferidas (Contexto)**: Roadmap actual, issues recientes

## Placeholders PM (para templates de uso manual)
- <PM_QUESTION>

## Ejemplo de Invocación
```
05-revisar-estado-del-proyecto-y-desalineaciones.md
PM_QUESTION="¿Qué procede con el error 500?"
```
