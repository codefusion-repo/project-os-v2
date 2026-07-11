# MOS-3.6 — Draft closeout commands

MOSDLC operation `draft-closeout-commands` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.review_before_close · mode.review_only · output.pm_command_bundle
- Evidence: evidence.issue_scope, evidence.pr_diff, evidence.validation_output
- PM approval: No (draft-only; the Human PM decides and runs the bundle)

**Does:** Draft copy-safe PR and issue closeout commands for the Human PM after review-before-close has resolved.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft copy-safe commands for the Human PM to comment, mark ready when applicable, merge, close, and clean up only when evidence supports it.

**Variables**
- Required: PR_NUMBER, ISSUE_NUMBER
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.pm_command_bundle. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.7. Next: MOS-3.9. Recommended: MOS-3.9.
