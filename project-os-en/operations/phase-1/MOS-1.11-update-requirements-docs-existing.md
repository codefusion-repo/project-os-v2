# MOS-1.11 — Update requirements docs existing

MOSDLC operation `update-requirements-docs-existing` · Phase 1 — Requirements, planning, and feasibility · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt (+output.draft_issue, output.status_result)
- Evidence: evidence.source_basis
- PM approval: Yes (exact approval for the file write only)

**Does:** Updates or creates requirements documentation for an existing project.
**For:** Close the documentary gap of adopted projects.
**How:** Same as MOS-1.4 but based on requirements extracted from the project.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: DOC_TARGET, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.route_prompt (+output.draft_issue, output.status_result). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-1.10. Next: MOS-1.12. Recommended: MOS-1.12.
