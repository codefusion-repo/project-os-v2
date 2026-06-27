# Draftear Comando para Crear Release Tag

## Objetivo de la Operación
Generar los comandos `git tag` y `git push --tags` de forma segura, basándose en la versión evaluada en la operación de readiness.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: TAG_NAME explícito o inferido de análisis previo.
- **Qué compara/decide**: Asegura que el tag no colisione con existentes.
- **Qué entrega (Output)**: PM command bundle con los comandos requeridos.
- **Qué NO debe hacer (Límites)**: Los agentes no ejecutan tags de manera automática. Autoridad exclusiva del PM.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (draftea). Humano PM (ejecuta y autoriza).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.release_readiness`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.pm_command_bundle`
- **Evidence Required**: `evidence.repo_state`

## Variables PM
- **Requeridas**: `TAG_NAME`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Último hash de main

## Placeholders PM (para templates de uso manual)
- <TAG_NAME>

## Ejemplo de Invocación
```
13-draftear-comando-para-crear-release-tag.md
TAG_NAME=VALOR_AQUI
```
