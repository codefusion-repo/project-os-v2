# Operating rules

## Two sources of truth

Stable operating behavior is versioned in `project-os-en/kernel/*.json` for the explicitly selected English surface. Live project facts—issues, PRs, branches, commits, reviews, checks, and deployments—remain in target systems of record and are read at task time. Memory, reports, and durable files are claims until verified.

## Resolution is not authorization

Actors, modes, workflows, outputs, artifacts, templates, variables, operations, and optional skills provide shape. Writes require a capable actor and mode, exact PM approval for the project/work unit/action, live evidence, preflight, proportional validation, and respected boundaries. Merge, closure, labels, tags, releases, settings, deployment, automation, and secret changes each require separate exact approval.

## Fail closed

Return exactly one configured status. Stop on an unknown surface, missing kernel data, conflicting sources, ambiguous authority, missing required evidence, failed required validation, or missing exact approval. Never invent state or add a fallback to conceal an unresolved primary path.

## Proportional validation

Use agent-run validation for kernel, resolver, tooling, security/privacy, authorization, traceability, deployment, migration, billing/storage, and deterministic contracts. Draft PM-run commands when execution should stay with the PM. Report manual PM validation for language, content, product judgment, UX, onboarding, and semantic parity. Add tests only for stable behavior and regression risk.

## Context economy and traceability

Use the smallest useful live evidence packet. Cite paths, lines, issues, PRs, diffs, or checks rather than copying full sources. Use subagents only for a scoped risk/complexity reason and verify their claims. Economy never removes required evidence, preflight, validation, secret safety, or approval.

## Secret safety

Never request, display, copy, summarize, store, commit, or upload secrets or secret-looking values. Use `[REDACTED]`; report only variable names, command names, paths, and risk types. Do not run broad environment/configuration dumps.

## Durable-content boundary

Kernel, docs, adapters, operations, templates, and skills never store live issue, PR, branch, commit, review, CI, validation, release, deployment, roadmap-readiness, or planning state.
