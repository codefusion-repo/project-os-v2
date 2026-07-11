# Security review prompt

```markdown
## Live context read
{{Issue, PR, repository, and surfaces.}}

## Review objective
{{Decision this review should enable.}}

## Recipient
{{Actual reviewer; not a kernel actor.}}

## Sensitive surfaces
- {{Auth, input, storage, dependency, admin, or deployment surface.}}

## Secret requirements
Never print, paste, upload, quote, summarize, or expose secret values. Use `[REDACTED]`.

## Evidence to review
- {{Path or live source.}}

## Findings format
- Severity · evidence · impact · safe route

## Out of scope
{{No fixes, deployment/settings, or secret-store changes without separate approval.}}
```
