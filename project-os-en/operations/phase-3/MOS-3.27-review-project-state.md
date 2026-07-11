# MOS-3.27 — Review PRoject state

MOSDLC operation `review-project-state` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Review PRoject status and misalignments with documentation.
**For:** Detect drift between docs, roadmap and repo reality.
**How:** Use PM decisions and fixed docs as the main truth.

**Variables**
- Required: — (none)
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: any phase. Next: MOS-3.1, MOS-3.3 or MOS-R.9. Recommended: MOS-R.9 if the drift is documentary.
