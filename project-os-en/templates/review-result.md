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

Before listing an observation as a finding, apply the materiality gate from
`rule.economia_de_contexto`: it is a finding only if it describes a verifiable
current state, an unsatisfied outcome, contract, risk, or capability, a concrete
materially improving action, and durable value. Something merely historical,
informational, confirmatory, already resolved by the normal course, or duplicated
from live evidence is omitted, or marked `invalid-finding` without routing if
already raised; a review may conclude with no findings even when it holds context
or observations.

- {{disposition: blocking-correction | non-blocking-follow-up | preference | accepted-risk | invalid-finding}} - {{file:line or reference}} - {{finding}}

Only `blocking-correction` requires correction before closure; a
`non-blocking-follow-up` requires a current, durable, actionable gap with
independent scope and a reason to defer it, and the other dispositions force no changes.

## Verdict or recommendation

{{GO, NO-GO, needs_context, follow-up or recommendation. On GO, the closeout
bundle and its final verification accompany this same response.}}

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
