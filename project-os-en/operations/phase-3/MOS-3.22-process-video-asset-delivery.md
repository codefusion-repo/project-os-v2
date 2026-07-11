# MOS-3.22 — PRocess video asset delivery

MOSDLC operation `process-video-asset-delivery` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Process delivered asset material or feedback into implementation, correction, or follow-up routing.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Classify DESIGN_DELIVERY into implementation route, correction route, follow-up issue, or no-op based on live product context.

**Variables**
- Required: DESIGN_DELIVERY
- Optional: ISSUE_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result (+output.route_prompt, output.pm_command_bundle). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.18. Next: MOS-3.4, MOS-3.5, MOS-3.3. Recommended: MOS-3.4.
