# MOS-R.6 — Create update adr from design

MOSDLC operation `create-update-adr-from-design` · Phase 2 — Design · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat a terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidence: evidence.source_basis
- PM approval: No for drafting; exact approval is required to write or update ADRs

**Does:** Create or update ADRs from design or requirements documentation, drafting the delegated write route per decision.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Extract stable, issue-surviving decisions from SOURCE_DOCS and draft one ADR (new or update) per decision, following the target repository's ADR conventions when present.

**Variables**
- Required: SOURCE_DOCS
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.route_prompt. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-2.6. Next: MOS-R.1. Recommended: MOS-R.1.
