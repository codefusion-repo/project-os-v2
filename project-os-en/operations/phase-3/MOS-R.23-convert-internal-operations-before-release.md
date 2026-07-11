# MOS-R.23 — Convert internal operations before release

MOSDLC operation `convert-internal-operations-before-release` · Phase 3 — Implementation · Risk: high.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat a terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt (+output.draft_issue)
- Evidence: evidence.source_basis
- PM approval: No for drafting; exact approval is required to convert, hide, remove, or disable

**Does:** Draft the removal, hiding, disabling, or conversion of the target's internal-only surfaces before a public release, as a delegated route.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft, per internal-only surface, the decision to remove, hide, disable, or convert it before the public release, with the evidence for each choice.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Safe options are remove, hide, disable, or convert; the specific choice may require the PM.
- Do not implement conversions or change packaging; this operation only drafts the route.
- Redact secrets and do not copy sensitive internal details outside their context.

**Deliver:** output.route_prompt (+output.draft_issue). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.22. Next: MOS-R.7. Recommended: MOS-R.7.
