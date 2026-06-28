# Analizar Readiness para Release o Tag

## Objetivo de la Operación
Evaluar si el estado actual del repositorio, los issues merged y la validación justifican la creación de un tag o release oficial.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Último tag, commits sin tag, changelog, validaciones CI/CD, estado vivo del repositorio.
- **Qué compara/decide**: Determina el impacto de los cambios (patch/minor/major) si falta TAG_NAME, evaluando riesgos y vacíos técnicos.
- **Qué entrega (Output)**: Recomendación de versión o reporte de brechas de release (readiness).
- **Qué NO debe hacer (Límites)**: No genera el tag, solo evalúa preparación.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (revisión PM-facing).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.release_readiness`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.status_result`
- **Evidence Required**: `evidence.repo_state, evidence.validation_output`

## Variables PM
- **Requeridas**: `Ninguna`
- **Opcionales**: `TAG_NAME`
- **Inferidas (Contexto)**: Diferencias vs tag anterior

## Placeholders PM (para templates de uso manual)
- <TAG_NAME>

## Ejemplo de Invocación
```
12-analizar-readiness-para-release-o-tag.md

```
