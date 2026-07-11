# MOS-2.6 — Validate design docs

MOSDLC operation `validate-design-docs` · Phase 2 — Design · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (read-only)

**Does:** Validate design documentation against Phase 1 requirements before implementation planning.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Check coverage, contradictions, missing design areas, unclear architecture or UI/UX choices, security gaps, and unresolved PM decisions.

**Variables**
- Required: — (none)
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-2.1, MOS-2.5. Next: MOS-R.4, MOS-3.1. Recommended: MOS-R.4.
