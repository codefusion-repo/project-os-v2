# MOS-R.21 — PRocess validation cycle findings

MOSDLC operation `process-validation-cycle-findings` · Phase 4 — QA and human verification · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (classifies and drafts; does not create or execute follow-ups)

**Does:** Process the findings of a validation cycle into bounded, traceable follow-ups, draft-only.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Classify each finding as blocking correction, non-blocking follow-up, product/roadmap feedback, or PM decision only when evidence supports that route.

**Variables**
- Required: VALIDATION_FINDINGS
- Optional: TARGET_REPOSITORY, VALIDATION_CYCLE_TYPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Findings may come from QA, UAT, beta, TestFlight, playtesting, integration, a pilot, or another target-owned cycle.
- Return `status.needs_pm_decision` when a finding changes product scope or direction.

**Deliver:** output.status_result (+drafts when applicable). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.20. Next: MOS-3.3. Recommended: MOS-3.3.
