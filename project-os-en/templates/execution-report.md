# Execution report

Responsibility: report executed work, evidence and validation without asking
merge/close.

PM-facing density: the resolver projects as `must_include` exactly the
`output.execution_report.must_include_by_density` list for the resolved
hydration level. Use only the block for the resolved level; never combine
levels. Receipt visibility follows
`context_receipt_contract.pm_facing_visibility` (`minimal` and `compact` hide
it; `full/debug` shows it); always keep the internal receipt intact at every
level.

## Minimal level

```markdown
## Result

{{What got done, in 1-3 lines.}}

## Files or surface

- {{Exact routes or touched surface.}}

## Validation

- `{{command}}` - {{actual result}}

## Reference

{{Live work unit, commit, or PR.}}
```

## Compact level

```markdown
## Scope

{{Implemented scope and respected out of scope, in 2-4 lines.}}

## Changes

- {{Material changes with exact routes.}}

## Validation

- `{{command}}` - {{actual result}}
- Not executed: {{reason if applicable}}
- Manual PM required: {{if applicable}}

## Risks

{{Remaining risks and accepted exceptions, or none.}}
```

## Full/debug level

```markdown
## Issue or PR

{{Unit of work.}}

## Repository

{{Repo target.}}

## Branch

{{Work branch.}}

## Evidence reviewed

- {{Issue/PR/roadmap/ADR/diff/comments read live.}}

## Files changed

- {{Exact routes.}}

## Validation

- `{{command}}` - {{actual result}}
- Not executed: {{reason if applicable}}
- Manual PM required: {{clarity/copy/UX/product if applicable}}

## Risks and limitations

{{Remaining risks, out-of-scope respected and exceptions accepted.}}

## Commit or PR

{{Reference if applicable.}}

## Remaining work

{{Follow-ups or none.}}

## Correction report (only when correcting a reviewed PR)

{{Publish as an append-only comment on the PR, without editing the body or any
prior comment or review.}}

- Source review or comment: {{exact reference to the review or comment}}
- Previous head: {{reviewed sha}}
- Corrected head: {{new sha}}
- Findings addressed: {{each blocking-correction with the change and its outcome}}
- Commits or range: {{reference}}
- No merge or close: {{confirmation that no merge or close happened}}

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
```
