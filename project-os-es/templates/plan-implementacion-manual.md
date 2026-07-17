# Plan de implementacion manual

Responsabilidad: draftear instrucciones humano-ejecutables sin reclamar edits.

```markdown
## Objetivo

{{Resultado esperado.}}

## Archivos a inspeccionar

- {{Ruta y razon.}}

## Archivos a modificar

- {{Ruta y ancla verificable.}}

## Plan de cambios

1. {{Cambio por archivo/ancla.}}

## Validacion

- `{{comando}}` - {{que debe probar}}

## QA manual

- {{Chequeo humano.}}

## Riesgos y rollback

{{Riesgos y como revertir.}}

## Siguiente operacion recomendada

{{Operacion Project OS.}}

## Declaracion de no escritura

Este plan no edito codigo, no ejecuto validacion y no concede permisos.

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

## Degradacion segura (solo si aplica)

- verified_evidence: {{Evidencia verificada.}}
- unavailable_evidence: {{Fuente no disponible.}}
- materiality: auxiliary
- decision_impact: {{Por que no cambia autoridad, scope ni decision material.}}
- equivalent_source_used: {{Fuente equivalente registrada o none.}}
- revalidation_required_before_write: true
```
