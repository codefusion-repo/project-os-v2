# Iniciar Bootstrap de Nuevo Proyecto

## Objetivo de la Operación
Draftear la estructura inicial para un repositorio totalmente nuevo, definiendo el roadmap inicial y la configuración del kernel.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Reglas de kernel, descripción inicial.
- **Qué compara/decide**: Define estructura vs mejores prácticas del kernel.
- **Qué entrega (Output)**: Plan de estructura, issue de roadmap fundacional.
- **Qué NO debe hacer (Límites)**: No asume que el terminal agent ya existe sin antes completar la adopción.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (planificación PM-facing).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.target_adoption`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.adoption_packet`
- **Evidence Required**: `evidence.target_adoption`

## Variables PM
- **Requeridas**: `TARGET_REPOSITORY`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Ninguna

## Placeholders PM (para templates de uso manual)
- <TARGET_REPOSITORY>

## Ejemplo de Invocación
```
02-iniciar-bootstrap-nuevo-proyecto.md
TARGET_REPOSITORY=VALOR_AQUI
```
