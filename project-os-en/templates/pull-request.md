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

Closes #{{issue}} (on PM merge decision).
```
