# Draftear Comando Crear Issue desde Descripción

## Objetivo de la Operación
Recibir una descripción de feature/bug por parte del PM y convertirla en un comando `gh issue create` con el formato Project OS adecuado.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: DESCRIPTION enviada por el PM.
- **Qué compara/decide**: Verifica que contenga el contexto necesario para un issue accionable.
- **Qué entrega (Output)**: Un PM command bundle con el comando `gh issue create ...` listo para ejecutar.
- **Qué NO debe hacer (Límites)**: El browser chat no ejecuta el comando, solo lo draftea.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (draft). Humano PM (ejecuta el bundle).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.pm_intake`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.pm_command_bundle`
- **Evidence Required**: `evidence.repo_state`

## Variables PM
- **Requeridas**: `DESCRIPTION`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Labels disponibles

## Placeholders PM (para templates de uso manual)
- <DESCRIPTION>

## Ejemplo de Invocación
```
04-draftear-comando-crear-issue-desde-descripcion.md
DESCRIPTION=VALOR_AQUI
```
