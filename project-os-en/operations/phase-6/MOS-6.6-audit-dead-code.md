# MOS-6.6 — Audit dead code

MOSDLC operation `audit-dead-code` · Phase 6 — Production readiness and maintenance · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Audit for orphaned code, legacy code, unused variables, obsolete functions, and dead code.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Identify orphaned modules, legacy code paths, unused variables, obsolete functions, and other dead code with concrete file and line evidence.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PATH_SCOPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: none. Next: MOS-6.12. Recommended: MOS-6.12.
