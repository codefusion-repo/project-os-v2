# MOS-3.30 — Draft manual implementation plan

MOSDLC operation `draft-manual-implementation-plan` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.issue_implementation_manual · mode.review_only · output.manual_implementation_plan
- Evidence: evidence.issue_scope, evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only; a human applies and validates)

**Does:** Draft a human-executable, step-by-step plan to implement an issue without writing files.
**For:** To deploy when no terminal agent is available or appropriate.
**How:** Provide a detailed plan by file and anchor; the plan never claims that code was edited.

**Variables**
- Required: ISSUE_NUMBER
- Optional: PATH_SCOPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Derived metadata:** the repository, the existing PR, and the branch are
reconstructed from the issue and are never asked of the PM. `PATH_SCOPE` stays
an input because it deliberately narrows the plan and is not derived from the
unit.

**Deliver:** output.manual_implementation_plan. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.1 or MOS-3.4 not available. Next: MOS-3.31. Recommended: MOS-3.31.
