# Paquete de adopcion

Responsabilidad: reportar auditoria o draft de adopcion de un target separando la
readiness browser de la terminal. Es draft-only: nunca prueba una mutacion ya
ejecutada; esa evidencia vive en `output.execution_report`. No guarda estado
vivo ni concede permisos.

```markdown
## Target repository

{{Repositorio target y lenguaje PM-facing.}}

## Version de kernel

{{Version declarada o tracks latest.}}

## Estado del roadmap

{{roadmap_state: present <owner/repo#N verificado> | missing. Cuando falta, no
inventes un numero ni rellenes {{#ROADMAP_ISSUE}} con placeholders durables.}}

## Estado de adopcion browser

{{browser_adoption_state: ready | drift | missing. El adapter browser es
PM-applied y no tiene por que existir como archivo del repo.}}

## Estado de adopcion terminal

{{terminal_adoption_state: ready | drift | missing | blocked_on_roadmap.}}

## Draft del adapter browser

{{Draft completo de BROWSER_CHAT.md aplicable por el PM, o nota de que ya esta
al dia. No pegues secretos ni estado vivo.}}

## Hallazgos del adapter terminal

{{Drift, faltantes o notas target-owned de AGENTS.md/CLAUDE.md/GEMINI.md; rutas y
resumen, sin secretos.}}

## Estado del route prompt

{{route_prompt_state: not_needed | blocked_on_roadmap | blocked_on_work_unit |
drafted. Un route prompt write-capable exige un roadmap vivo y una unidad de
trabajo viva; nunca se inventan.}}

## Acciones manuales del PM

- {{Lo que el PM aplica o entrega a mano: pegar el adapter browser, crear el
  roadmap con el bundle, entregar el route prompt.}}

## Acciones del agente

- {{Lo que un terminal agent ejecutaria solo bajo route prompt entregado con
  aprobacion exacta; el draft por si mismo no autoriza.}}

## Constraints target-owned

{{Producto, dominio, build, validacion y constraints que quedan en el target.}}

## Validacion

- {{Validacion y verificacion PM/agent.}}

## Rollback

{{Restaurar adapters previos o revertir PR.}}
```
