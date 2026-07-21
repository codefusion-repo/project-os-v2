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

{{roadmap_state: present <owner/repo#N verificado> | missing. El roadmap es
evidencia viva opcional, nunca prerequisito de adopcion. Cuando falta, no
inventes un numero ni lo guardes como configuracion durable del adapter.}}

## Estado de adopcion browser

{{browser_adoption_state: ready | drift | missing. El adapter browser es
PM-applied y no tiene por que existir como archivo del repo.}}

## Estado de adopcion terminal

{{terminal_adoption_state: ready | drift | missing.}}

## Draft del adapter browser

{{Draft completo de BROWSER_CHAT.md aplicable por el PM, o nota de que ya esta
al dia. No pegues secretos ni estado vivo.}}

## Hallazgos del adapter terminal

{{Drift, faltantes o notas target-owned de AGENTS.md/CLAUDE.md/GEMINI.md; rutas y
resumen, sin secretos.}}

## Estado del route prompt

{{route_prompt_state: not_needed | blocked_on_target_scope | drafted. Un route
prompt write-capable exige la unidad viva de adopcion acotada por target, scope
de adapters y rama, mas branch preflight, validacion y aprobacion PM exacta al
entregarse; no exige roadmap ni issue previos y nunca se inventa el scope.}}

## Acciones manuales del PM

- {{Lo que el PM aplica o entrega a mano: pegar el adapter browser, entregar el
  route prompt y, si lo decide, crear el roadmap con el bundle.}}

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
