# MOS-R.6 — Create or update an ADR from design

MOSDLC operation `create-update-adr-from-design` · Phase 2 — Design · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat a terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidence: evidence.source_basis
- PM approval: No for drafting; exact approval is required to write or update ADRs

**Does:** Extract stable decisions from design or requirements documentation and draft ADRs.
**For:** To preserve in ADRs the decisions that must survive documents and issues.
**How:** Read SOURCE_DOCS, identify candidate decisions, and derive a delegated path for each decision.

**Variables**
- Required: SOURCE_DOCS
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.route_prompt. In case of unreadable docs, absence of stable decisions or conflict with existing ADR, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-2.6 or design update. Next: MOS-R.1 by extracted decision. Recommended: MOS-R.1.
