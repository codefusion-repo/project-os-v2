# MOS-R.2 — Recommend next operation

MOSDLC operation `recommend-next-operation` · Cross-phase — Accepted recommended operations · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (recommendation only; does not execute or authorize)

**Does:** Recommend the next MOSDLC operation from live traceability, recommendation-only.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Read-only analysis of live traceability to recommend exactly one next MOSDLC operation, with the evidence that supports it and safe alternatives when the evidence is ambiguous.

**Variables**
- Required: — (none)
- Optional: TARGET_REPOSITORY, ISSUE_NUMBER, PR_NUMBER, ROADMAP_ISSUE, CURRENT_STATUS, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: none. Next: none. Recommended: none.
