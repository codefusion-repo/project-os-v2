# Actualizar Adopción de Kernel en Target

## Objetivo de la Operación
Llevar un repositorio que ya adoptó Project OS a una versión de kernel más reciente, actualizando los adaptadores (AGENTS.md, CLAUDE.md, GEMINI.md) sin sobrescribir notas, restricciones de seguridad/dominio ni comandos de validación propios del target.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Adaptadores actuales del target, la versión de kernel adoptada declarada, la versión vigente del kernel canónico, anclas de roadmap.
- **Qué compara/decide**: Detecta drift de versión, baseline obsoleto y mismatch de roadmap entre el adaptador del target y el kernel canónico.
- **Qué entrega (Output)**: Un `output.adoption_packet` con el diff de actualización de adaptadores y un checklist; el PR solo si el modo y la aprobación PM exacta lo permiten.
- **Qué NO debe hacer (Límites)**: No toca código de producto, no migra estado vivo a archivos durables, no cambia visibilidad/settings, no ejecuta merge/tag/release y no borra notas, restricciones ni comandos de validación propios del target.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (draftea el diff y el checklist de actualización). Secundaria: `terminal_agent` (aplica la actualización solo si es ruteado con route-prompt + `mode.delegated_commit_pr` + aprobación PM exacta).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.target_adoption`
- **Execution Mode**: `mode.delegated_commit_pr`
- **Output Contract**: `output.adoption_packet`
- **Evidence Required**: `evidence.target_adoption`

## Variables PM
- **Requeridas**: `TARGET_REPOSITORY`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Versión de kernel adoptada vs versión vigente

## Placeholders PM (para templates de uso manual)
- <TARGET_REPOSITORY>

## Ejemplo de Invocación
```
23-actualizar-adopcion-de-kernel-en-target.md
TARGET_REPOSITORY=VALOR_AQUI
```
