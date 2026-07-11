# MOS-R.4 — Review phase readiness

MOSDLC operation `review-phase-readiness` · Cross-phase · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (advisory review; does not change phase)

**Does:** Review readiness advisory before moving work between MOSDLC phases.
**For:** To identify evidence, blockers and missing decisions before moving forward.
**How:** Contrast current phase, target phase and live state without executing transition.

**Variables**
- Required: — (none)
- Optional: CURRENT_PHASE, TARGET_PHASE, ISSUE_NUMBER, PR_NUMBER, TARGET_REPOSITORY, ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If there is evidence of a missing phase or ambiguous transition, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: closure or review of a phase. Next: safe operation of the target phase; MOS-R.3 if PM decision is missing; MOS-R.2 if routing is missing. Recommended: Safe operation of the target phase when ready.
