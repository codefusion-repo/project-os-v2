# Resultado de estado

Responsabilidad: devolver un estado y, cuando MOS-R.3 procesa una decisión PM,
su resolución canónica sin rellenar con reglas repetidas.

Presentación PM-facing: aplica `context_receipt_contract.pm_facing_visibility`
al bloque marcado; conserva siempre el recibo interno íntegro.

```markdown
## Estado

{{status.resolved | status.needs_context | status.needs_pm_decision | status.blocked}}

## Resolución de decisión PM (solo si aplica)

- decision_key: {{proyecto/target · unidad · acción material · alcance exacto}}
- superseded_decision: {{decisión anterior única más reciente, exacta y suficiente; ninguna si empata}}
- current_pm_decision: {{decisión vigente o ninguna}}
- required_traceability_follow_up: {{drift durable a reconciliar o ninguno}}
- remaining_gates: {{gates independientes y su estado}}
- resulting_status: {{estado seleccionado}}
- safe_return_operation: {{operación origen segura}}

## Falta, conflicto o bloqueo

{{Que falta o bloquea exactamente.}}

## Fuente o decision requerida

{{De donde debe venir o quien decide.}}

## Siguiente paso seguro

{{Paso minimo que preserva limites.}}

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
