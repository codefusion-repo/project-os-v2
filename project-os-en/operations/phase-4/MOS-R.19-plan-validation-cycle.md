# MOS-R.19 — Plan validation cycle

MOSDLC operation `plan-validation-cycle` · Phase 4 — QA and human verification · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.draft_issue (+output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (planning only; the PM starts the cycle)

**Does:** Plan a real validation cycle for the target project, drafting the plan and its bounded issues for Human PM execution.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft the validation-cycle plan for the applicable surface: goals, entry criteria, bounded scope, participants or evidence sources, exit criteria, and how findings will be captured.

**Variables**
- Required: — (none)
- Optional: TARGET_REPOSITORY, VALIDATION_CYCLE_TYPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Keep the wording target-agnostic: web, mobile, games, libraries/tools, and internal products may use different cycles.
- Fail closed if the target has no applicable validation surface or the PM must choose between surfaces.

**Deliver:** output.draft_issue (+output.pm_command_bundle). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-4.1, MOS-4.2. Next: MOS-R.20. Recommended: MOS-R.20.
