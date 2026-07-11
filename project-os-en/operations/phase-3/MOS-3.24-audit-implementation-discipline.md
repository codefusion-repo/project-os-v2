# MOS-3.24 — Audit implementation discipline

MOSDLC operation `audit-implementation-discipline` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.implementation_discipline_audit · mode.review_only · output.review_result (+output.draft_issue)
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Audit implementation discipline gaps against boundary.implementation_discipline.
**For:** Detect discipline debt with file and line evidence.
**How:** Read-only audit with findings and follow-up drafts.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PATH_SCOPE, FOCUS, ISSUE_NUMBER, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.review_result (+output.draft_issue). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: any phase. Next: MOS-3.26. Recommended: MOS-3.26.
