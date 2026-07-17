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

## Planned evolution: evidence materiality and safe degradation

**This section documents a planned requirement, not implemented behavior.** Until this evolution exists in the kernel, the current behavior described above remains unchanged: on missing or ambiguous required evidence, the system stops fail-closed.

**Objective.** In a future evolution, distinguish the evidence that supports a hard gate from auxiliary context evidence, so that partial unavailability of the latter can degrade safely, explicitly, and traceably instead of always forcing a total block, without weakening any material gate.

- **Hard gates vs. auxiliary evidence (future distinction).** Exact PM approval, branch preflight, required validation, target identity, exact SHA/ref, and secret safety will keep failing closed without exception. The planned distinction would apply only to auxiliary context evidence, never to a hard gate.
- **Equivalent sources.** When the primary source of an auxiliary piece of evidence is unavailable, a verifiable equivalent source could satisfy the same requirement, recording which source was used and why.
- **Connector failures.** A connector, API, or network failure while reading auxiliary evidence should degrade explicitly, never silently: the result names what could not be read and confirms which gates remain intact.
- **Drafts with deferred revalidation.** A draft could proceed with incomplete auxiliary evidence only if it is marked for deferred revalidation, and that revalidation must complete before any material action.
- **Explicit gaps.** Every degradation leaves named, visible gaps in the corresponding output, within the kernel's existing statuses; completeness is never declared while hiding a gap.

**Acceptance criteria for the future implementation:**

1. No current hard gate is weakened or made degradable.
2. The material/auxiliary classification of each piece of evidence is defined deterministically in the kernel and protected by tests.
3. Every degradation is explicit, traceable, and revalidatable; silent failures remain forbidden.
4. Until that approved implementation exists, today's total fail-closed behavior is preserved intact.
