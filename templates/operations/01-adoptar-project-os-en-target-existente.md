# Adoptar Project OS en Target Existente

## Objetivo de la Operación
Preparar un repositorio existente para operar con Project OS, añadiendo el adaptador AGENTS.md y configurando las herramientas iniciales.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Repositorio definido en TARGET_REPOSITORY.
- **Qué compara/decide**: Detecta qué archivos de adopción faltan en el target.
- **Qué entrega (Output)**: Un PR o un plan de adopción (adoption packet).
- **Qué NO debe hacer (Límites)**: No toca código de producto, no modifica visibilidad, no altera el kernel principal.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (draftea plan). Secundaria: `terminal_agent` (implementa si se le rutea).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.target_adoption`
- **Execution Mode**: `mode.delegated_commit_pr`
- **Output Contract**: `output.adoption_packet`
- **Evidence Required**: `evidence.target_adoption`

## Variables PM
- **Requeridas**: `TARGET_REPOSITORY`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Estado de adaptadores en el target

## Placeholders PM (para templates de uso manual)
- <TARGET_REPOSITORY>

## Ejemplo de Invocación
```
01-adoptar-project-os-en-target-existente.md
TARGET_REPOSITORY=VALOR_AQUI
```
