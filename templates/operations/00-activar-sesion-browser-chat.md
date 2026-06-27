# Activar sesión Browser Chat

## Objetivo de la Operación
Iniciar la sesión del PM en browser chat, establecer el contexto del kernel y las reglas de draft-only.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Estado del repo, kernel base.
- **Qué compara/decide**: Verifica que el actor activo sea `actor.browser_chat`.
- **Qué entrega (Output)**: Contexto inicial establecido, listo para recibir operaciones o PM_QUESTION.
- **Qué NO debe hacer (Límites)**: No realiza commits, no ejecuta comandos locales, no modifica el sistema.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat`. (No interviene terminal_agent).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.review_only`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.status_result`
- **Evidence Required**: `evidence.repo_state`

## Variables PM
- **Requeridas**: `Ninguna`
- **Opcionales**: `PM_QUESTION`
- **Inferidas (Contexto)**: Contexto de GitHub

## Placeholders PM (para templates de uso manual)
- <PM_QUESTION>

## Ejemplo de Invocación
```
00-activar-sesion-browser-chat.md
PM_QUESTION="¿Qué procede con el error 500?"
```
