# MOS-R.1 — Record adr decision

MOSDLC operation `record-adr-decision` · Phase 2 — Design · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat a terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidence: evidence.source_basis
- PM approval: No for drafting; exact approval is required to write the ADR

**Does:** Draft an ADR that records a stable PM decision plus the delegated write route for a terminal agent.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft the ADR content (context, decision, consequences) from DECISION and its evidence basis, following the target repository's ADR conventions when present.

**Variables**
- Required: DECISION
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.route_prompt. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.6. Next: MOS-3.1. Recommended: MOS-3.1.
