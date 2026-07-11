# MOS-3.7 — Review PR before close

MOSDLC operation `review-pr-before-close` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_before_close · mode.review_only · output.review_result (+output.pm_command_bundle)
- Evidence: evidence.issue_scope, evidence.pr_diff, evidence.validation_output
- PM approval: No (does not merge or close; drafts closure only after a resolved review)

**Does:** Review the PR against the linked issue before drafting closure and cleanup.
**For:** Quality gate prior to any closure.
**How:** Compare the diff, validation, and scope; use execution reports as evidence leads.

**Variables**
- Required: PR_NUMBER
- Optional: EXECUTION_REPORT, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.review_result (+output.pm_command_bundle). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.4 or MOS-3.5. Next: MOS-3.6 if resolves; MOS-3.5 if there are findings. Recommended: MOS-3.6.
