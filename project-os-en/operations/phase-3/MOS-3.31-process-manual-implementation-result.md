# MOS-3.31 — Process manual implementation result

MOSDLC operation `process-manual-implementation-result` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.issue_scope, evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Process the result of the manual implementation applied by the human.
**For:** To classify the safe route after applying a manual plan.
**How:** Refer to PR review when a PR exists; do not duplicate that review.

**Variables**
- Required: ISSUE_NUMBER, MANUAL_IMPLEMENTATION_RESULT
- Optional: MANUAL_IMPLEMENTATION_PLAN, PR_NUMBER, TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result (+output.route_prompt, output.pm_command_bundle). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.30. Next: MOS-3.7 if there is PR; MOS-3.5 or MOS-3.3 if not. Recommended: MOS-3.7 if there is PR.
