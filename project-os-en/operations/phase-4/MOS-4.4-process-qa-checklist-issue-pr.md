# MOS-4.4 — Process an issue/PR QA checklist

MOSDLC operation `process-qa-checklist-issue-pr` · Phase 4 — QA and human verification · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Process the issue/PR human-checklist result.
**For:** To convert human QA into correction, follow-up or advancement.
**How:** Classify blockers and non-blockers without executing anything.

**Variables**
- Required: QA_RESULT
- Optional: ISSUE_NUMBER, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result (+output.route_prompt, output.pm_command_bundle). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-4.1. Next: MOS-4.8, MOS-4.7 or MOS-3.7. Recommended: MOS-4.8 for blockers.
