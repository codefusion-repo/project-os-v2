# Draftear Paquete de Handoff para Nueva Sesión

## Objetivo de la Operación
Recuperar el contexto clave de una conversación larga, decisiones PM humano recientes y estado de GitHub, para transferirlo al inicio de un chat nuevo.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Conversación actual, decisiones PM, estado vivo del código.
- **Qué compara/decide**: Identifica qué información no está aún en un PR/Issue duradero.
- **Qué entrega (Output)**: Un mensaje compacto (handoff packet) que un humano PM puede copiar y pegar en otra sesión de chat.
- **Qué NO debe hacer (Límites)**: No guarda esto como un archivo duradero (`.txt` local); la memoria es GitHub.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (síntesis de memoria volátil).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.handoff`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.handoff_packet`
- **Evidence Required**: `evidence.repo_state`

## Variables PM
- **Requeridas**: `Ninguna`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Decisiones en el contexto del chat

## Placeholders PM (para templates de uso manual)
- <NINGUNA>

## Ejemplo de Invocación
```
17-draftear-paquete-de-handoff-para-nueva-sesion.md

```
