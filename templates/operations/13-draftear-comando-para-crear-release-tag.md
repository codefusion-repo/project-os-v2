# Draftear Comando para Crear Release Tag

## Objetivo de la Operación
Generar los comandos `git tag` y `git push --tags` de forma segura, basándose en la versión evaluada en la operación de readiness.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: TAG_NAME explícito si el PM lo provee; si falta, el tag recomendado derivado de la operación de readiness.
- **Qué compara/decide**: Asegura que el tag no colisione con existentes y que la versión sea coherente con el readiness.
- **Qué entrega (Output)**: PM command bundle con `git tag` y `git push --tags`. Si falta TAG_NAME, se detiene en la recomendación de readiness y NO emite los comandos finales de ejecución.
- **Qué NO debe hacer (Límites)**: El browser chat solo draftea; los agentes no ejecutan tags. La ejecución de los comandos de tag es autoridad exclusiva del Humano PM.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (draftea). Humano PM (ejecuta y autoriza).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.release_readiness`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.pm_command_bundle`
- **Evidence Required**: `evidence.repo_state, evidence.validation_output`

## Variables PM
- **Requeridas**: `Ninguna`
- **Opcionales**: `TAG_NAME`
- **Inferidas (Contexto)**: TAG_NAME recomendado desde `release_readiness` cuando falta; último hash de main

## Placeholders PM (para templates de uso manual)
- <TAG_NAME>

## Ejemplo de Invocación
```
13-draftear-comando-para-crear-release-tag.md
TAG_NAME=VALOR_AQUI
```
