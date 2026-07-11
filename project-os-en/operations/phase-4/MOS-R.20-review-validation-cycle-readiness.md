# MOS-R.20 — Review validation cycle readiness

MOSDLC operation `review-validation-cycle-readiness` · Phase 4 — QA and human verification · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (advisory review; the PM starts or closes the cycle)

**Does:** Review readiness to start or close a validation cycle for the target project, read-only and advisory.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Read-only advisory review of the cycle's entry criteria (to start) or exit criteria (to close), listing missing evidence, unresolved blockers, and pending PM decisions.

**Variables**
- Required: — (none)
- Optional: TARGET_REPOSITORY, VALIDATION_CYCLE_TYPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.19. Next: MOS-R.21. Recommended: MOS-R.21.
