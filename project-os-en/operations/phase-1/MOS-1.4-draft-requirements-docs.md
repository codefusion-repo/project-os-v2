# MOS-1.4 — Draft requirements docs

MOSDLC operation `draft-requirements-docs` · Phase 1 — Requirements, planning, and feasibility · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt (+output.draft_issue, output.status_result)
- Evidence: evidence.source_basis
- PM approval: Yes (exact approval for the file write only)

**Does:** Draft documentation of functional and non-functional requirements, use cases and user stories.
**For:** To establish the documentary base for Phase 1.
**How:** Draft in browser chat; a terminal agent applies the changes only with exact approval.

**Variables**
- Required: — (none)
- Optional: DOC_TARGET, TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.route_prompt (+output.draft_issue, output.status_result). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-1.2, MOS-1.3. Next: MOS-1.5. Recommended: MOS-1.5.
