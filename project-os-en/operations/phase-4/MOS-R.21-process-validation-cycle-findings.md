# MOS-R.21 — Process validation cycle findings

MOSDLC operation `process-validation-cycle-findings` · Phase 4 — QA and human verification · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (classifies and drafts; does not create or execute follow-ups)

**Does:** Process validation-cycle findings and convert them into limited follow-ups.
**For:** To capture real friction from the target as traceable work.
**How:** Classify findings by evidence, impact, and route: correction, follow-up, PM decision, or no-op.

**Variables**
- Required: VALIDATION_FINDINGS
- Optional: TARGET_REPOSITORY, VALIDATION_CYCLE_TYPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Findings may come from QA, UAT, beta, TestFlight, playtesting, integration, a pilot, or another target-owned cycle.
- Return `status.needs_pm_decision` when a finding changes product scope or direction.

**Deliver:** output.status_result (+drafts if applicable). For unreadable findings or without evidence base, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.20 at the end of the cycle. Next: MOS-3.3 by finding. Recommended: MOS-3.3.
