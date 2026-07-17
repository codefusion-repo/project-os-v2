# Operating rules

## Two sources of truth

Stable operating behavior is versioned in `project-os-en/kernel/*.json` for the explicitly selected English surface. Live project facts—issues, PRs, branches, commits, reviews, checks, and deployments—remain in target systems of record and are read at task time. Memory, reports, and durable files are claims until verified.

## Resolution is not authorization

Actors, modes, workflows, outputs, artifacts, templates, variables, operations, and optional skills provide shape. Writes require a capable actor and mode, exact PM approval for the project/work unit/action, live evidence, preflight, proportional validation, and respected boundaries. Merge, closure, labels, tags, releases, settings, deployment, automation, and secret changes each require separate exact approval.

## Fail closed

Return exactly one configured status. Stop on an unknown surface, missing kernel data, conflicting sources, ambiguous authority, missing minimum or material evidence, failed required validation, or missing exact approval. Never invent state or add a fallback to conceal an unresolved primary path.

## Proportional validation

Use agent-run validation for kernel, resolver, tooling, security/privacy, authorization, traceability, deployment, migration, billing/storage, and deterministic contracts. Draft PM-run commands when execution should stay with the PM. Report manual PM validation for language, content, product judgment, UX, onboarding, and semantic parity. Add tests only for stable behavior and regression risk.

## Context economy and traceability

Use the smallest useful live evidence packet. Cite paths, lines, issues, PRs, diffs, or checks rather than copying full sources. Use subagents only for a scoped risk/complexity reason and verify their claims. Economy never removes required evidence, preflight, validation, secret safety, or approval.

The normal reading surface starts at the manifest and is limited to the selected resolution, applicable limits and evidence, output and artifact, exact template, requested skills, minimum live evidence, and target sources required by scope, validation, or source basis. Internal tooling, resolver-projected metadata, actual model context, and post-resolution reads are separate categories. Every execution reports them through `context_receipt.minimum_read_surface` in the output envelope alongside the artifact, using repository-relative paths or live identifiers and reasons rather than absolute machine paths or full bodies. Reads outside the normal surface require `full/debug`, audit, debugging, security/authorization review, complex architecture, or a concrete PM decision; no reason replaces evidence or gates.

## Secret safety

Never request, display, copy, summarize, store, commit, or upload secrets or secret-looking values. Use `[REDACTED]`; report only variable names, command names, paths, and risk types. Do not run broad environment/configuration dumps.

## Durable-content boundary

Kernel, docs, adapters, operations, templates, and skills never store live issue, PR, branch, commit, review, CI, validation, release, deployment, roadmap-readiness, or planning state.

## Evidence materiality and safe degradation

The active contract distinguishes `material` from `auxiliary` evidence. Each workflow declares `required_evidence`, the set it must attempt to obtain and report, and `minimum_evidence`, the material minimum for its action. Each output declares an `action_class` and whether it accepts non-material gaps.

- **Non-degradable hard gates.** Exact PM approval, branch preflight, required validation, target identity, exact SHA/ref, secret safety, privacy, real source conflicts, and all material evidence remain fail-closed. A mutable output never accepts gaps.
- **One representation.** Only an `action.read_only` or `action.draft_only` output with `allows_non_material_gaps: true` may reuse `status.resolved`. It must expose `verified_evidence`, `unavailable_evidence`, `materiality`, `decision_impact`, `equivalent_source_used`, and `revalidation_required_before_write`. It cannot claim completion while gaps remain.
- **Equivalent sources.** An alternative satisfies evidence only when the contract declares it, its verification criteria are met, and the substitution is recorded. CI is equivalent only for the same exact SHA/ref and validation scope; it is never presumed equivalent to the real merge.
- **Unavailability is not state.** Connector, API, or network errors—including 404, 422, and 502—mean the source is unavailable; they do not prove target absence, closure, merge, failure, or nonexistence.
- **Material truncation.** A truncated response blocks when the missing portion may change authority, scope, or the decision. If that impact cannot be classified, fail closed.
- **Revalidation before writes.** Every gap, including an auxiliary one, must be fully revalidated before editing, committing, pushing, opening a PR, merging, closing, tagging, deploying, or executing any other mutation.
