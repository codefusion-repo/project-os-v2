# MOS-3.9 — Verify post merge

MOSDLC operation `verify-post-merge` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Verify post-merge repository and issue state without mutating GitHub or git.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Check that default branch, linked issue, merged PR state, and relevant validation evidence are consistent after merge.

**Variables**
- Required: PR_NUMBER
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.6. Next: MOS-3.1, MOS-3.10. Recommended: MOS-3.1.
