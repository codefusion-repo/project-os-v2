# Review result

Responsibility: report findings or verdict supported by evidence.

PM-facing traceability: `Reviewed evidence` is the canonical representation. Do
not add a receipt block.

```markdown
## Reviewed scope

{{Issue/PR/surface.}}

## Evidence reviewed

- {{Diff, final files, comments, validation, docs. For QA/readiness: same unit,
  target, covered ref and environment; reused/renewed evidence with source and
  reason under the common continuity contract.}}

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

{{GO, NO-GO, needs_context, follow-up, or recommendation. Only resolved GO from
workflow.review_before_close delivers closeout and verification in this response.
Readiness identifies next action, responsible party, evidence, exact approval,
applicable rollback, and postconditions; it authorizes neither release nor deploy.}}

## Risks

{{Residual risks.}}

## Not reviewed

{{Explicit gaps.}}

## Safe degradation (when applicable)

- verified_evidence: {{Verified evidence.}}
- unavailable_evidence: {{Unavailable source.}}
- materiality: auxiliary
- decision_impact: {{Why authority, scope, and the material decision are unchanged.}}
- equivalent_source_used: {{Recorded equivalent source or none.}}
- revalidation_required_before_write: true
```
