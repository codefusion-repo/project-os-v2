# MOS-3.9 — Verify post-merge state

MOSDLC operation `verify-post-merge` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Verify that the main branch was healthy and the issue was resolved after the merge.
**For:** To close the implementation loop with evidence.
**How:** Read-only check of default branch, issue and checks.

**Variables**
- Required: PR_NUMBER
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.6. Next: MOS-3.1 or MOS-3.10. Recommended: MOS-3.1.
