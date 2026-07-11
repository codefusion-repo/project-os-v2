# MOS-4.1 — Draft an issue/PR QA checklist

MOSDLC operation `draft-qa-checklist-issue-pr` · Phase 4 — QA and human verification · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Draft the human QA checklist focused on an issue/PR.
**For:** To cover non-automatable checks with directed human QA.
**How:** Extract issue/PR criteria in human-verifiable steps.

**Variables**
- Required: ISSUE_NUMBER
- Optional: PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.7. Next: MOS-4.4. Recommended: MOS-4.4.
