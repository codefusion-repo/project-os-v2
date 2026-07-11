# MOS-3.30 — Draft manual implementation plan

MOSDLC operation `draft-manual-implementation-plan` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.issue_implementation_manual · mode.review_only · output.manual_implementation_plan
- Evidence: evidence.issue_scope, evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only; a human applies and validates)

**Does:** Draft a human-executable implementation plan for one scoped issue without editing files.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft output.manual_implementation_plan with objective, files to inspect, files to modify, anchored change plan, reasoning, validation commands, manual QA, risks, rollback, and next operation.

**Variables**
- Required: ISSUE_NUMBER
- Optional: TARGET_REPOSITORY, PATH_SCOPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.manual_implementation_plan. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.1, MOS-3.4. Next: MOS-3.31. Recommended: MOS-3.31.
