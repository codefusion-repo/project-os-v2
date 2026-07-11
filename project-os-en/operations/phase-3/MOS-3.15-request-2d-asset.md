# MOS-3.15 — Request a 2D asset

MOSDLC operation `request-2d-asset` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → external_recipient
- Kernel: workflow.design_asset · mode.review_only · output.asset_prompt
- Evidence: evidence.repo_state, evidence.source_basis
- PM approval: No (the route prompt does not authorize; writing requires exact PM approval)

**Does:** Draft the asset prompt to request a 2D asset from an external recipient.
**For:** Get 2D assets without treating the creator as a kernel actor.
**How:** Prompt PM-facing with objective, constraints and delivery format.

**Variables**
- Required: DESCRIPTION
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.asset_prompt. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: asset need detected. Next: MOS-3.19 upon arrival of delivery. Recommended: MOS-3.19.
