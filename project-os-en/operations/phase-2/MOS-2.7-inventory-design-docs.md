# MOS-2.7 — Inventory design docs

MOSDLC operation `inventory-design-docs` · Phase 2 — Design · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.target_adoption
- PM approval: No (read-only)

**Does:** Identifies the existing design documentation in a project.
**For:** Know what design already exists before creating or updating.
**How:** Read-only inventory of design docs and their status.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-1.12. Next: MOS-2.8. Recommended: MOS-2.8.
