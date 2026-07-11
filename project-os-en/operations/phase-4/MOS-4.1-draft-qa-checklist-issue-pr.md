# MOS-4.1 — Draft qa checklist issue pr

MOSDLC operation `draft-qa-checklist-issue-pr` · Phase 4 — QA and human verification · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Draft a human QA checklist for an issue or PR without executing QA.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Extract human-verifiable flows, edge cases, accessibility or UX checks, and acceptance criteria from live evidence.

**Variables**
- Required: ISSUE_NUMBER
- Optional: PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.7. Next: MOS-4.4. Recommended: MOS-4.4.
