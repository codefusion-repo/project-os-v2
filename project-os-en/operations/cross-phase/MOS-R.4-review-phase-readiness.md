# MOS-R.4 — Review phase readiness

MOSDLC operation `review-phase-readiness` · Cross-phase — Accepted recommended operations · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (advisory review; does not change phase)

**Does:** Review advisory readiness before moving between MOSDLC phases, without executing any transition.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Read-only advisory review of readiness to move from CURRENT_PHASE toward TARGET_PHASE, listing missing evidence, pending PM decisions, and blockers.

**Variables**
- Required: — (none)
- Optional: CURRENT_PHASE, TARGET_PHASE, ISSUE_NUMBER, PR_NUMBER, TARGET_REPOSITORY, ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: none. Next: MOS-R.3, MOS-R.2. Recommended: none.
