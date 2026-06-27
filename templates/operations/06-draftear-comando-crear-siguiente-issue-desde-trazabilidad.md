# Draftear Comando Crear Siguiente Issue desde Trazabilidad Viva

## Objetivo de la Operación
Reconstruir el estado a partir de issues abiertos, cerrados, PRs, y el roadmap para inferir cuál es el próximo outcome real y draftear su creación.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Roadmap (`<ROADMAP_ISSUE>`), estado actual, decisiones previas del PM.
- **Qué compara/decide**: Compara progreso logrado vs planeado en el roadmap.
- **Qué entrega (Output)**: Un bundle de comando `gh issue create` para un (1) único issue específico, no un backlog amplio inventado.
- **Qué NO debe hacer (Límites)**: No inventa issues no derivados explícitamente de la trazabilidad viva.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (draftea bundle). Humano PM (ejecuta).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.pm_intake`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.pm_command_bundle`
- **Evidence Required**: `evidence.repo_state`

## Variables PM
- **Requeridas**: `Ninguna`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: El siguiente paso del roadmap

## Placeholders PM (para templates de uso manual)
- <NINGUNA>

## Ejemplo de Invocación
```
06-draftear-comando-crear-siguiente-issue-desde-trazabilidad.md

```
