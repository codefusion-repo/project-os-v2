# Pull request

Responsibility: document claims, scope and validation of a PR draft. It is not
completeness test until review against diff/final files.

PM-facing traceability: `Validation` and the declared scope are the canonical
representation. Do not add a receipt block; detailed provenance is delivered only
when the PM asks for it for audit, debugging, security or authorization review,
or investigating an incorrect resolution.

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

Related to #{{issue}}.
```
