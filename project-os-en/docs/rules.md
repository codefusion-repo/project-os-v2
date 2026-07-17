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
- **Minimum sufficient evidence per output and action.** The future implementation defines, for each output and each material action, what minimum evidence is sufficient to proceed; anything beyond that minimum is auxiliary context whose absence is recorded as an explicit gap, not as an automatic block.
- **Material impact of each gap.** Each gap declares its impact on the decision it supports: what could not be verified and whether it affects authority, scope, or only context. A truncated comment, for example, blocks only when the truncated part affects the authority or scope of the decision.
- **Safe resolution with explicit non-material gaps.** The future implementation must allow a safe resolution with explicit, visible non-material gaps in the output; the definitive technical name of that resolution is decided in that implementation, not in this document. Completeness is never declared while hiding a gap.
- **Equivalent sources.** When the primary source of an auxiliary piece of evidence is unavailable, a verifiable equivalent source could satisfy the same requirement, recording which source was used and why.
- **Connector failures.** A connector, API, or network failure while reading auxiliary evidence degrades explicitly, never silently. Errors such as 404, 422, or 502 are treated as source unavailability, not as target state: the result names what could not be read and confirms which gates remain intact.
- **Read-only drafts with mandatory revalidation.** A read-only draft may proceed with incomplete auxiliary evidence only if it is marked for mandatory revalidation, and that revalidation must complete before any mutation.

**Acceptance criteria for the future implementation:**

1. No current hard gate is weakened or made degradable.
2. The material/auxiliary classification and the minimum sufficient evidence per output and action are defined deterministically in the kernel and protected by tests.
3. Every degradation is explicit, traceable, and revalidatable; silent failures remain forbidden.
4. The minimum test cases cover: missing auxiliary evidence, missing exact approval, equivalent source, truncated response, draft with partial evidence, tag without SHA, real decision conflict, and CI equivalent to the real merge.
5. Until that approved implementation exists, today's total fail-closed behavior is preserved intact.
