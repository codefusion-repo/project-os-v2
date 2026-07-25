# Resultado de revision

Responsabilidad: reportar hallazgos o veredicto respaldado por evidencia.

Presentación PM-facing: aplica `context_receipt_contract.pm_facing_visibility`
al bloque marcado; conserva siempre el recibo interno íntegro.

```markdown
## Scope revisado

{{Issue/PR/superficie.}}

## Evidencia revisada

- {{Diff, archivos finales, comentarios, validacion, docs.}}

## Comparacion contra scope

{{Mapa breve de objetivo/scope/out-of-scope/acceptance contra evidencia.}}

## Hallazgos

Antes de listar una observacion como hallazgo, aplica el gate de materialidad de
`rule.economia_de_contexto`: solo es hallazgo si describe un estado actual
verificable, un outcome, contrato, riesgo o capacidad insatisfecho, una accion
concreta de mejora material y valor durable. Lo meramente historico, informativo,
confirmatorio, ya resuelto por el curso normal o duplicado de evidencia viva se
omite, o se marca `invalid-finding` sin routing si ya fue elevado; un review puede
concluir sin hallazgos aunque contenga contexto u observaciones.

- {{disposicion: blocking-correction | non-blocking-follow-up | preference | accepted-risk | invalid-finding}} - {{archivo:linea o referencia}} - {{hallazgo}}

Solo `blocking-correction` exige correccion antes del cierre; un
`non-blocking-follow-up` requiere un gap vigente, durable y accionable con scope
independiente y razon para diferirlo, y las demas disposiciones no fuerzan cambios.

## Veredicto o recomendacion

{{GO, NO-GO, needs_context, follow-up o recomendacion. Con GO, el bundle de
closeout y su verificacion final acompanan esta misma respuesta.}}

## Riesgos

{{Riesgos residuales.}}

## No revisado

{{Gaps explicitos.}}

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

## Degradacion segura (solo si aplica)

- verified_evidence: {{Evidencia verificada.}}
- unavailable_evidence: {{Fuente no disponible.}}
- materiality: auxiliary
- decision_impact: {{Por que no cambia autoridad, scope ni decision material.}}
- equivalent_source_used: {{Fuente equivalente registrada o none.}}
- revalidation_required_before_write: true
```
