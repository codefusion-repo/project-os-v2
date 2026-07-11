# MOS-3.20 — Process a 3D asset delivery

MOSDLC operation `process-3d-asset-delivery` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Processes the delivery of a 3D asset and maps it to technical tasks or drafts.
**For:** Integrate assets received into the development cycle.
**How:** Classify the delivery into an issue, correction, or follow-up.

**Variables**
- Required: DESIGN_DELIVERY
- Optional: ISSUE_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result (+output.route_prompt, output.pm_command_bundle). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.16. Next: MOS-3.4, MOS-3.5 or MOS-3.3. Recommended: MOS-3.4.
