# MOS-3.31 — PRocess manual implementation result

MOSDLC operation `process-manual-implementation-result` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.issue_scope, evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Classify the result of human-applied manual implementation without claiming browser-chat execution.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Classify MANUAL_IMPLEMENTATION_RESULT into PR review, correction route, follow-up issue, PM decision, readiness review, or no-op.

**Variables**
- Required: ISSUE_NUMBER, MANUAL_IMPLEMENTATION_RESULT
- Optional: MANUAL_IMPLEMENTATION_PLAN, PR_NUMBER, TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result (+output.route_prompt, output.pm_command_bundle). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.30. Next: MOS-3.7, MOS-3.5, MOS-3.3. Recommended: MOS-3.7.
