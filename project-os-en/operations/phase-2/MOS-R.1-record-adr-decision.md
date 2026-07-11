# MOS-R.1 — Record an ADR decision

MOSDLC operation `record-adr-decision` · Phase 2 — Design · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat a terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidence: evidence.source_basis
- PM approval: No for drafting; exact approval is required to write the ADR

**Does:** Draft an ADR to record a stable PM decision and the delegated write path.
**For:** To preserve decisions that must survive the current issue.
**How:** Convert DECISION and its basis into non-authorizing ADR and route-prompt content.

**Variables**
- Required: DECISION
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.route_prompt. In case of missing, ambiguous, no evidence or unapproved writing decision, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.6 or stable PM decision. Next: MOS-3.1 when the decision is recorded. Recommended: MOS-3.1.
