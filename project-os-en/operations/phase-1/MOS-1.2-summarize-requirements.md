# MOS-1.2 — Summarize requirements

MOSDLC operation `summarize-requirements` · Phase 1 — Requirements, planning, and feasibility · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result
- Evidence: evidence.source_basis
- PM approval: No (draft-only)

**Does:** Summarize and structure the requirements identified in the interview.
**For:** To have a stable foundation before documenting.
**How:** Synthesize the conversation into a list verifiable by the PM.

**Variables**
- Required: — (none)
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-1.1. Next: MOS-1.3. Recommended: MOS-1.3.
