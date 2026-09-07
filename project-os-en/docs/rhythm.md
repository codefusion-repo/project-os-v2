# Lifecycle rhythm

## Proportionality: four levels of work

Classify work before picking operations; the class governs unit, PR, review,
validation, and report density:

- **Level 0 — Reading or analysis.** Direct answer with sufficient evidence;
  no unit, roadmap, branch, tests, or durable artifact.
- **Level 1 — Small reversible change.** An exact, verifiable PM instruction
  may be the live unit when the target allows it: preflight, scoped branch,
  the complete solution that best satisfies the outcome, sufficient minimal
  validation, `minimal` report.
  No issue, roadmap, ADR, new tests, or new tooling by default.
- **Level 2 — Standard change.** The core loop below.
- **Level 3 — Critical or hard-to-revert change.** Kernel, authorization,
  security, migrations, deployment, releases, public contracts: formal unit,
  PR, independent review, rollback, and broad validation.

Issues, PRs, branches, and GitHub are available adapters, never universal
requirements of the model.

[Work unit continuity](../operations/README.md#primary-work-unit-continuity)
spans planning, implementation, review, QA, correction, handoff, and closeout.
Required QA precedes GO: MOS-4.1 → MOS-4.4 reuses MOS-3.5 for correction of the
same PR and MOS-3.3 for material, independent follow-ups grouped by outcome.
MOS-4.8/MOS-4.7 retain compatible QA entry points consuming those contracts in
the same response. For sequential roadmaps, MOS-3.1 verifies predecessor
completion before drafting a single next unit; another phase or separate
approval does not create units.

## Core loop for standard changes

1. Reconstruct the live roadmap, work unit, repository, and prior decisions.
2. Use a PM-intake operation to draft one bounded unit or route prompt.
3. Resolve `workflow.issue_implementation` with the exact allowed mode.
4. Run branch preflight before the first edit; work only on `work/<unit>-<slug>`.
5. Implement the complete solution that best satisfies the scope's outcome and run proportional validation.
6. Commit, push, and open a draft PR only when the mode and exact PM approval allow it.
7. Run `workflow.review_before_close` against the real changed files, diff, relevant final files, validation, and linked unit; give every finding a disposition — only `blocking-correction` returns to correction, and each correction is recorded as an append-only correction report (source review, previous and corrected heads, findings, validation) without editing the body or prior comments before the next review.
8. Leave merge and closure with the PM; on GO the review delivers the closeout bundle and its final verification in the same response, and a separate postcondition verification (merge, final SHA, closure, cleanup) via MOS-3.27 remains for failures, audits, or an explicit PM request.

## Alternate branches

- Intake and design: requirements, feasibility, docs, ADRs, and roadmap operations.
- Manual implementation: browser chat drafts a human-executable plan and never claims edits.
- QA/security/assets: draft recipient prompts or classify evidence-backed results; no implied writes.
- Deployment: use only target-owned commands for one exactly approved environment; production stays with the Human PM by default.
- Maintenance: convert validated findings into bounded corrections, issues, or no-op decisions.

Each operation declares previous, next, and recommended MOS codes. Those links guide routing and never authorize the next action.
