# MOS-R.20 — Review validation cycle readiness

MOSDLC operation `review-validation-cycle-readiness` · Phase 4 — QA and human verification · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (advisory review; the PM starts or closes the cycle)

**Does:** Check readiness to start or close a target validation cycle.
**For:** Enter and exit validation with clear criteria.
**How:** Evaluate entry or exit criteria, missing evidence, blockers and pending PM decisions.

**Variables**
- Required: — (none)
- Optional: TARGET_REPOSITORY, VALIDATION_CYCLE_TYPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. In case of unreadable criteria or evidence, or pending start/close decision, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.19 or cycle in progress. Next: MOS-R.21 when closing the cycle. Recommended: MOS-R.21 when findings exist.
