# Draftear Comando para Crear Release de GitHub

## Objetivo de la Operación
Generar un PM command bundle con `gh release create` para publicar un objeto Release de GitHub (notas + tag asociado), distinto del simple tag de git que produce la operación de release tag.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Readiness previo, último tag/release, commits desde el último release, notas/changelog candidatos, validaciones.
- **Qué compara/decide**: Confirma que existe o se recomienda un TAG_NAME y que las notas reflejan los outcomes merged; evita colisión con releases existentes.
- **Qué entrega (Output)**: PM command bundle con `gh release create`. Si falta TAG_NAME, se detiene en la recomendación derivada del readiness y NO emite el comando final de publicación.
- **Qué NO debe hacer (Límites)**: El browser chat solo draftea; el Humano PM ejecuta y autoriza la publicación. No publica releases, no etiqueta ni hace merge por su cuenta.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (draftea el bundle). Humano PM (ejecuta y autoriza).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.release_readiness`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.pm_command_bundle`
- **Evidence Required**: `evidence.repo_state`

## Variables PM
- **Requeridas**: `Ninguna`
- **Opcionales**: `TAG_NAME`
- **Inferidas (Contexto)**: TAG_NAME recomendado desde `release_readiness` cuando falta; notas derivadas de los commits merged

## Placeholders PM (para templates de uso manual)
- <TAG_NAME>

## Ejemplo de Invocación
```
24-draftear-comando-crear-release-github.md
TAG_NAME=VALOR_AQUI
```
