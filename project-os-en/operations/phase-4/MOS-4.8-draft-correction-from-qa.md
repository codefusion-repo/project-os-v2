# MOS-4.8 — Draft a correction from QA

MOSDLC operation `draft-correction-from-qa` · Phase 4 — QA and human verification · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (the route prompt does not authorize; writing requires exact PM approval)

**Does:** Draft the correction prompt from QA results.
**For:** To fix QA blockers without expanding the scope.
**How:** Encapsulate QA_RESULT in a delegated correction path.

**Variables**
- Required: QA_RESULT
- Optional: ISSUE_NUMBER, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.route_prompt. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-4.4. Next: MOS-3.7. Recommended: MOS-3.7.
