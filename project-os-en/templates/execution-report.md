# Execution report

Responsibility: report executed work, evidence and validation without asking
merge/close.

PM-facing presentation: apply `context_receipt_contract.pm_facing_visibility`
to the marked block; always keep the internal receipt intact. PM-facing
density follows `context_receipt_contract.pm_facing_density` by hydration
level: `minimal` reports result, files or surface, validation, and reference;
`compact` reports scope, changes, validation, and risks; `full/debug` uses the
full contract below with the receipt visible.

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
