# MOS-4.5 — Process QA checklist feature

MOSDLC operation `process-qa-checklist-feature` · Phase 4 — QA and human verification · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Process the human description-or-feature checklist result.
**For:** To close the features QA loop without anchor issue.
**How:** Classify findings into a new issue, correction, or no-op.

**Variables**
- Required: QA_RESULT
- Optional: DESCRIPTION, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result (+output.route_prompt, output.pm_command_bundle). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-4.2. Next: MOS-3.8 or MOS-4.7. Recommended: MOS-3.8 if new work is created.
