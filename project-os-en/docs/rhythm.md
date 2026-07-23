# Lifecycle rhythm

## Proportionality: four levels of work

Classify work before picking operations; the class governs unit, PR, review,
validation, and report density:

- **Level 0 — Reading or analysis.** Direct answer with sufficient evidence;
  no unit, roadmap, branch, tests, or durable artifact.
- **Level 1 — Small reversible change.** An exact, verifiable PM instruction
  may be the live unit when the target allows it: preflight, scoped branch,
  smallest complete solution, sufficient minimal validation, `minimal` report.
  No issue, roadmap, ADR, new tests, or new tooling by default.
- **Level 2 — Standard change.** The core loop below.
- **Level 3 — Critical or hard-to-revert change.** Kernel, authorization,
  security, migrations, deployment, releases, public contracts: formal unit,
  PR, independent review, rollback, and broad validation.

Issues, PRs, branches, and GitHub are available adapters, never universal
requirements of the model.

## Core loop for standard changes

1. Reconstruct the live roadmap, work unit, repository, and prior decisions.
2. Use a PM-intake operation to draft one bounded unit or route prompt.
3. Resolve `workflow.issue_implementation` with the exact allowed mode.
4. Run branch preflight before the first edit; work only on `work/<unit>-<slug>`.
5. Implement the smallest complete solution for the scope and run proportional validation.
6. Commit, push, and open a draft PR only when the mode and exact PM approval allow it.
7. Run `workflow.review_before_close` against the real changed files, diff, relevant final files, validation, and linked unit; give every finding a disposition — only `blocking-correction` returns to correction.
8. Leave merge and closure with the PM; on GO the review delivers the closeout bundle and its final verification in the same response, and separate post-merge verification remains for failures, audits, or an explicit PM request.

## Alternate branches

- Intake and design: requirements, feasibility, docs, ADRs, and roadmap operations.
- Manual implementation: browser chat drafts a human-executable plan and never claims edits.
- QA/security/assets: draft recipient prompts or classify evidence-backed results; no implied writes.
- Deployment: use only target-owned commands for one exactly approved environment; production stays with the Human PM by default.
- Maintenance: convert validated findings into bounded corrections, issues, or no-op decisions.

Each operation declares previous, next, and recommended MOS codes. Those links guide routing and never authorize the next action.
