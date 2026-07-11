# MOS-1.9 — Review requirement removal

MOSDLC operation `review-requirement-removal` · Phase 1 — Requirements, planning, and feasibility · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (read-only)

**Does:** Review the impact of removing a requirement from the project.
**For:** Avoid removals that break roadmap, docs or dependencies.
**How:** Analyzes impact and returns decision to the PM; fail-closed to status.needs_pm_decision.

**Variables**
- Required: DESCRIPTION
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-1.7. Next: MOS-1.8 if PM confirms. Recommended: MOS-1.8 if PM confirms removal.
