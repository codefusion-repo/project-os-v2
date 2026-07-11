# Skill: backend architecture

## Responsibility

Apply backend judgment to architecture, data, APIs, security, performance, reliability, migrations, and observability while preserving the live issue scope.

## When to use it

Use for service boundaries, data models, APIs, background work, cloud infrastructure, integrations, migrations, concurrency, resilience, or backend performance. Do not select it merely because a repository has a backend.

## Quality criteria

- Make ownership and boundaries explicit; keep one source of truth for each invariant.
- Define API success and failure semantics, validation, authorization, idempotency, pagination, and compatibility.
- Enforce authorization server-side per resource, not only in UI or routing layers.
- Design data changes with constraints, transactional behavior, migration/rollback paths, and concurrency in mind.
- Bound retries, timeouts, queues, caches, and external calls; expose actionable observability without sensitive values.
- Validate risk proportionally, including deterministic contracts and failure paths.

## Risks to detect

Data loss, unsafe migrations, broken idempotency, authorization gaps, race conditions, unbounded work, N+1 queries, cache incoherence, ambiguous ownership, hidden fallback paths, secret exposure, and operational behavior without health evidence.

## Decisions to favor

Prefer explicit primary paths, boring interfaces, stable error contracts, database constraints, small reversible migrations, least privilege, bounded resource use, and telemetry that names events and risk types without secrets.

## Examples of judgment

### Stable API errors

Use a documented machine-readable error code and appropriate status, while keeping internal details out of the response. Validate the contract rather than string snapshots.

### Per-resource authorization

Load the requested resource, evaluate the caller's action against that resource and tenancy, then proceed. A role check detached from resource ownership is insufficient.

### Idempotent retryable writes

Bind an idempotency key to actor, operation, and normalized input; persist the first result atomically; reject conflicting reuse; and expire keys under an explicit retention rule.

## Expected output

Return scoped recommendations or findings with evidence, tradeoffs, validation, risks, and a safe next step. Do not turn the skill into a separate workflow.

## Limits / non-authorization

This skill is optional. It grants no permission and never replaces live scope, PM approval, branch preflight, evidence, validation, traceability, or review-before-close.
