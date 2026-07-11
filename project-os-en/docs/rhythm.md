# Lifecycle rhythm

## Core issue-to-draft-PR loop

1. Reconstruct the live roadmap, issue, repository, and prior decisions.
2. Use a PM-intake operation to draft one bounded issue or route prompt.
3. Resolve `workflow.issue_implementation` with the exact allowed mode.
4. Run branch preflight before the first edit; work only on `work/<unit>-<slug>`.
5. Implement the complete scoped behavior and run proportional validation.
6. Commit, push, and open a draft PR only when the mode and exact PM approval allow it.
7. Run `workflow.review_before_close` against the real changed files, diff, relevant final files, validation, and linked issue.
8. Leave merge and closure with the PM; verify post-merge state through a separate read-only operation.

## Alternate branches

- Intake and design: requirements, feasibility, docs, ADRs, and roadmap operations.
- Manual implementation: browser chat drafts a human-executable plan and never claims edits.
- QA/security/assets: draft recipient prompts or classify evidence-backed results; no implied writes.
- Deployment: use only target-owned commands for one exactly approved environment; production stays with the Human PM by default.
- Maintenance: convert validated findings into bounded corrections, issues, or no-op decisions.

Each operation declares previous, next, and recommended MOS codes. Those links guide routing and never authorize the next action.
