# MOS-2.8 — Audit design doc gaps

MOSDLC operation `audit-design-doc-gaps` · Phase 2 — Design · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.source_basis
- PM approval: No (read-only)

**Does:** Audit gaps between existing design documentation and Phase 1 requirements.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Compare current design docs against Phase 1 requirements and classify missing, stale, contradictory, or under-specified design areas.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-2.7. Next: MOS-2.9, MOS-2.13. Recommended: none.
