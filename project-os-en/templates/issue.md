# Issue

Responsibility: draft a verifiable unit of work with one outcome per issue.

```markdown
## Why it exists

{{1-3 sentences of the real problem.}}

## Objective

{{Observable result upon closing.}}

## Source basis

- {{Roadmap, issues, PRs, ADRs or source decisions.}}

## Scope

- {{Included. Maximum practical and verifiable.}}

## Out of scope

- {{Only plausible errors that the agent could try.}}

## Included decisions

{{Binding PM decisions if they exist; skip if not applicable.}}

## Acceptance criteria

- {{Observable criteria.}}

## Validation

- {{Agent-run, PM-run, manual PM or no automated with reason.}}

## Risk and rollback

{{Brief risk. Rollback: revert the PR when applicable.}}

## Safe degradation (when applicable)

- verified_evidence: {{Verified evidence.}}
- unavailable_evidence: {{Unavailable source.}}
- materiality: auxiliary
- decision_impact: {{Why authority, scope, and the material decision are unchanged.}}
- equivalent_source_used: {{Recorded equivalent source or none.}}
- revalidation_required_before_write: true
```

Do not keep live status or secret values.
