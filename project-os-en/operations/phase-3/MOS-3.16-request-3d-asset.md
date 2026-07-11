# MOS-3.16 — Request 3d asset

MOSDLC operation `request-3d-asset` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → external_recipient
- Kernel: workflow.design_asset · mode.review_only · output.asset_prompt
- Evidence: evidence.repo_state, evidence.source_basis
- PM approval: No (the route prompt does not authorize; writing requires exact PM approval)

**Does:** Draft an external-recipient asset request prompt without treating the recipient as a kernel actor.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft output.asset_prompt with source context, asset objective, asset type, usage context, dimensions, format, accessibility, acceptance criteria, and out-of-scope limits.

**Variables**
- Required: DESCRIPTION
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.asset_prompt. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: none. Next: MOS-3.20. Recommended: MOS-3.20.
