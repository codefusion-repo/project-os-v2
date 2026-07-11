# MOS-1.2 — Summarize requirements

MOSDLC operation `summarize-requirements` · Phase 1 — Requirements, planning, and feasibility · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result
- Evidence: evidence.source_basis
- PM approval: No (draft-only)

**Does:** Summarize and structure identified requirements into a PM-verifiable basis before documentation or planning.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Group requirements into functional, non-functional, constraints, assumptions, dependencies, and open questions.

**Variables**
- Required: — (none)
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-1.1. Next: MOS-1.3. Recommended: MOS-1.3.
