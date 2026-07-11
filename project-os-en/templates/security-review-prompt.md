# Security review prompt

Responsibility: request OWASP review without running scanners or exposing secrets.

```markdown
## Live-read context

{{Issue/PR/repo/surfaces.}}

## Review objective

{{What decision should you enable.}}

## Recipient

{{Real reviewer; not kernel actor.}}

## Sensitive surfaces

- Auth/authorization/sessions.
- Input validation, uploads, redirects.
- Dependencies, admin, logging, errors and config.

## Secret-safety requirements

Do not print, paste, upload, quote or summarize secrets. Write values as
`[REDACTED]`; report only route, variable and type of risk.

## Evidence to review

- {{Files, diffs, docs, checks.}}

## Finding format

- {{severity}} - {{reference}} - {{risk}} - {{expected remediation}}

## Out of scope

{{No fixes, no deploy/settings, no secret-store changes without separate approval.}}
```
