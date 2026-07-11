# MOS-2.12 — Update coding standards docs

MOSDLC operation `update-coding-standards-docs` · Phase 2 — Design · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt (+output.draft_issue, output.status_result)
- Evidence: evidence.source_basis
- PM approval: Yes (exact approval for the file write only)

**Does:** Draft updates or creation routes for coding standards documentation from existing docs and Phase 1 requirements.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft coding standards updates that preserve valid existing conventions and close evidence-backed gaps.

**Variables**
- Required: — (none)
- Optional: SOURCE_DOCS, DOC_TARGET, TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.route_prompt (+output.draft_issue, output.status_result). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-2.8. Next: MOS-2.14. Recommended: MOS-2.14.
