# Analizar Idea como Feature del Sistema

## Objetivo de la Operación
Evaluar propuestas abstractas para determinar su encaje dentro del kernel, roadmap, y código actual sin forzar la creación inmediata de un issue.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: IDEA dada por el PM, documentación arquitectural (DESIGN.md), estado vivo.
- **Qué compara/decide**: Determina viabilidad, riesgos, redundancias, y posibles ubicaciones en el código.
- **Qué entrega (Output)**: Diagnóstico de factibilidad y próximos pasos recomendados.
- **Qué NO debe hacer (Límites)**: No convierte la idea automáticamente en un issue sin una decisión explícita del PM.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (review conceptual y arquitectura).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.review_only`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.status_result`
- **Evidence Required**: `evidence.repo_state`

## Variables PM
- **Requeridas**: `IDEA`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Documentos de diseño actuales

## Placeholders PM (para templates de uso manual)
- <IDEA>

## Ejemplo de Invocación
```
16-analizar-idea-como-feature-del-sistema.md
IDEA=VALOR_AQUI
```
