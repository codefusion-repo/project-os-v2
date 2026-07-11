# MOS-3.6 — Draft closeout commands

MOSDLC operation `draft-closeout-commands` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.review_before_close · mode.review_only · output.pm_command_bundle
- Evidence: evidence.issue_scope, evidence.pr_diff, evidence.validation_output
- PM approval: No (draft-only; the Human PM decides and runs the bundle)

**Does:** Draft the issue/PR closure and cleanup package according to live status.
**For:** Close with complete evidence and without agent-side writes.
**How:** Copy-safe bundle that runs the Human PM.

**Variables**
- Required: PR_NUMBER, ISSUE_NUMBER
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.pm_command_bundle. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.7. Next: MOS-3.9. Recommended: MOS-3.9.
