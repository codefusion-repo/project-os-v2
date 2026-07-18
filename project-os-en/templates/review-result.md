# Review result

Responsibility: report findings or verdict supported by evidence.

PM-facing presentation: apply `context_receipt_contract.pm_facing_visibility`
to the marked block; always keep the internal receipt intact.

```markdown
## Reviewed scope

{{Issue/PR/surface.}}

## Evidence reviewed

- {{Diff, final files, comments, validation, docs}}

## Scope comparison

{{Short map of objective/scope/out-of-scope/acceptance versus evidence.}}

## Findings

- {{severity}} - {{file:line or reference}} - {{finding}}

## Verdict or recommendation

{{GO, NO-GO, needs_context, follow-up or recommendation.}}

## Risks

{{Residual risks.}}

## Not reviewed

{{Explicit gaps.}}

<!-- context-receipt:pm-facing-conditional -->
## Source receipt

- project_os_sources_read: {{List of source + reason, or [].}}
- target_sources_read: {{List of source + reason, or [].}}
- live_evidence_sources: {{List of source + reason, or [].}}
- resolved_template: {{Exact path or none.}}
- requested_skills: {{List of key + source, or [].}}
- tool_internal_sources: {{List of source + reason, or [].}}
- resolver_projected_metadata: {{List of source + reason, or [].}}
- model_context_sources: {{List of source + incorporation, or [].}}
- additional_context_reason: {{Allowed value or none.}}
<!-- /context-receipt -->

## Safe degradation (when applicable)

- verified_evidence: {{Verified evidence.}}
- unavailable_evidence: {{Unavailable source.}}
- materiality: auxiliary
- decision_impact: {{Why authority, scope, and the material decision are unchanged.}}
- equivalent_source_used: {{Recorded equivalent source or none.}}
- revalidation_required_before_write: true
```
