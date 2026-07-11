# MOS-2.8 — Audit design doc gaps

MOSDLC operation `audit-design-doc-gaps` · Phase 2 — Design · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.source_basis
- PM approval: No (read-only)

**Does:** Identify gaps in the existing documentation with respect to Phase 1.
**For:** Prioritize which design to update or create.
**How:** Compare inventory against requirements and list gaps.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-2.7. Next: MOS-2.9 to MOS-2.13 depending on gap. Recommended: the main gap update operation.
