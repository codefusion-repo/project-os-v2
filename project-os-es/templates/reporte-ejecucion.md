# Reporte de ejecucion

Responsabilidad: reportar trabajo ejecutado, evidencia y validacion sin pedir
merge/cierre.

Presentación PM-facing: aplica `context_receipt_contract.pm_facing_visibility`
al bloque marcado; conserva siempre el recibo interno íntegro. La densidad
PM-facing sigue `context_receipt_contract.pm_facing_density` según el nivel de
hidratación: `minimal` reporta resultado, archivos o superficie, validación y
referencia; `compact` reporta scope, cambios, validación y riesgos; `full/debug`
usa el contrato completo de abajo con el recibo visible.

```markdown
## Issue o PR

{{Unidad de trabajo.}}

## Repositorio

{{Repo target.}}

## Rama

{{Rama de trabajo.}}

## Evidencia revisada

- {{Issue/PR/roadmap/ADR/diff/comentarios leidos vivo.}}

## Archivos cambiados

- {{Rutas exactas.}}

## Validacion

- `{{comando}}` - {{resultado real}}
- No ejecutada: {{razon si aplica}}
- Manual PM requerida: {{claridad/copy/UX/producto si aplica}}

## Riesgos y limitaciones

{{Riesgos restantes, out-of-scope respetado y excepciones aceptadas.}}

## Commit o PR

{{Referencia si aplica.}}

## Trabajo restante

{{Follow-ups o ninguno.}}

<!-- context-receipt:pm-facing-conditional -->
## Recibo de fuentes

- project_os_sources_read: {{Lista de source + reason, o [].}}
- target_sources_read: {{Lista de source + reason, o [].}}
- live_evidence_sources: {{Lista de source + reason, o [].}}
- resolved_template: {{Path exacto o none.}}
- requested_skills: {{Lista de key + source, o [].}}
- tool_internal_sources: {{Lista de source + reason, o [].}}
- resolver_projected_metadata: {{Lista de source + reason, o [].}}
- model_context_sources: {{Lista de source + incorporation, o [].}}
- additional_context_reason: {{Valor permitido o none.}}
<!-- /context-receipt -->
```
