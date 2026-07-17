# Pull request

Responsibility: document claims, scope and validation of a PR draft. It is not
completeness test until review against diff/final files.

```markdown
## Summary

- {{What changes in terms of behavior.}}

## Scope / Boundaries

- {{Touched surfaces.}}
- {{Out of scope preserved.}}
- Merge and closure are not requested by this PR.

## Validation

- `{{command}}` - {{actual result}}
- {{manual PM validation or exception accepted if applicable.}}

## Security / Privacy

- {{Handling sensitive data or "no sensitive surfaces touched."}}

## Source Receipt

- project_os_sources_read: {{List of source + reason, or [].}}
- target_sources_read: {{List of source + reason, or [].}}
- live_evidence_sources: {{List of source + reason, or [].}}
- resolved_template: project-os-en/templates/pull-request.md
- requested_skills: {{List of key + source, or [].}}
- tool_internal_sources: {{List of source + reason, or [].}}
- resolver_projected_metadata: {{List of source + reason, or [].}}
- model_context_sources: {{List of source + incorporation, or [].}}
- additional_context_reason: {{Allowed value or none.}}

Closes #{{issue}} (on PM merge decision).
```
