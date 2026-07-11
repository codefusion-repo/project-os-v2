# MOS-4.8 — Draft correction from qa

MOSDLC operation `draft-correction-from-qa` · Phase 4 — QA and human verification · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (the route prompt does not authorize; writing requires exact PM approval)

**Does:** Draft a non-authorizing correction route prompt from blocking QA results without expanding scope.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Summarize blocking QA findings and map each one to original issue, PR, or acceptance evidence.

**Variables**
- Required: QA_RESULT
- Optional: ISSUE_NUMBER, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.route_prompt. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-4.4. Next: MOS-3.7. Recommended: MOS-3.7.
