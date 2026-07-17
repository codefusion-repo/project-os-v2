# Resultado de revision

Responsabilidad: reportar hallazgos o veredicto respaldado por evidencia.

```markdown
## Scope revisado

{{Issue/PR/superficie.}}

## Evidencia revisada

- {{Diff, archivos finales, comentarios, validacion, docs.}}

## Comparacion contra scope

{{Mapa breve de objetivo/scope/out-of-scope/acceptance contra evidencia.}}

## Hallazgos

- {{severity}} - {{archivo:linea o referencia}} - {{hallazgo}}

## Veredicto o recomendacion

{{GO, NO-GO, needs_context, follow-up o recomendacion.}}

## Riesgos

{{Riesgos residuales.}}

## No revisado

{{Gaps explicitos.}}

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
