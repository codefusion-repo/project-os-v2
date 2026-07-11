# MOS-R.2 — Recommend next operation

MOSDLC operation `recommend-next-operation` · Cross-phase · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (recommendation only; does not execute or authorize)

**Does:** Recommend exactly one next MOSDLC operation from live traceability.
**For:** Choose lifecycle path without ad hoc reasoning.
**How:** Read live status, justify the recommendation and show safe alternatives if there is ambiguity.

**Variables**
- Required: — (none)
- Optional: TARGET_REPOSITORY, ISSUE_NUMBER, PR_NUMBER, ROADMAP_ISSUE, CURRENT_STATUS, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. In the event of insufficient or unreadable traceability, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: any operation that requires routing. Next: the recommended operation, invoked by the Human PM. Recommended: The recommended operation.
