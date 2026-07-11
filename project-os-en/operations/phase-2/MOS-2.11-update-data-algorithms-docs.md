# MOS-2.11 — Update data algorithms docs

MOSDLC operation `update-data-algorithms-docs` · Phase 2 — Design · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt (+output.draft_issue, output.status_result)
- Evidence: evidence.source_basis
- PM approval: Yes (exact approval for the file write only)

**Does:** Update or create data structure and algorithm documentation from existing documentation and Phase 1.
**For:** Sustain Phase 2 with stable design documentation.
**How:** Browser chat drafts; a terminal agent applies the changes only with exact approval.

**Variables**
- Required: — (none)
- Optional: SOURCE_DOCS, DOC_TARGET, TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.route_prompt (+output.draft_issue, output.status_result). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-2.8. Next: MOS-2.14. Recommended: MOS-2.14.
