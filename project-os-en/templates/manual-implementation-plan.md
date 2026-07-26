# Manual implementation plan

Responsibility: draft human-executable instructions without claiming edits.

PM-facing traceability: `Files to inspect` and the anchored plan are the
canonical representation. Do not add a receipt block.

```markdown
## Objective

{{Expected result.}}

## Files to inspect

- {{Route and reason.}}

## Files to modify

- {{Verifiable route and anchor.}}

## Change plan

1. {{Change per file/anchor}}

## Validation

- `{{command}}` - {{which you should try}}

## Manual QA

- {{Human check.}}

## Risks and rollback

{{Risks and how to reverse.}}

## Recommended next operation

{{Operation Project OS.}}

## No-write statement

This plan did not edit code, did not run validation and did not grant permissions.

## Safe degradation (when applicable)

- verified_evidence: {{Verified evidence.}}
- unavailable_evidence: {{Unavailable source.}}
- materiality: auxiliary
- decision_impact: {{Why authority, scope, and the material decision are unchanged.}}
- equivalent_source_used: {{Recorded equivalent source or none.}}
- revalidation_required_before_write: true
```
