# MOS-3.13 — Audit traceability

MOSDLC operation `audit-traceability` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Audit live issue and PR traceability to confirm the implementation cycle is reconstructible from evidence.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Check whether issue, PRs, commits, comments, review, validation, and closure evidence reconstruct the work accurately.

**Variables**
- Required: ISSUE_NUMBER
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: none. Next: MOS-3.14. Recommended: MOS-3.14.
