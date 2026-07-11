# MOS-3.17 — Request audio asset

MOSDLC operation `request-audio-asset` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → external_recipient
- Kernel: workflow.design_asset · mode.review_only · output.asset_prompt
- Evidence: evidence.repo_state, evidence.source_basis
- PM approval: No (the route prompt does not authorize; writing requires exact PM approval)

**Does:** Draft the asset prompt to request an audio asset from an external recipient.
**For:** Get audio assets without treating the creator as a kernel actor.
**How:** Prompt PM-facing with objective, constraints and delivery format.

**Variables**
- Required: DESCRIPTION
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.asset_prompt. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: asset need detected. Next: MOS-3.21 upon delivery arrival. Recommended: MOS-3.21.
