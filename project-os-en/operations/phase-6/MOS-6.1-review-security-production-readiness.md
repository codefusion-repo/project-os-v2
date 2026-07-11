# MOS-6.1 — Review security production readiness

MOSDLC operation `review-security-production-readiness` · Phase 6 — Production readiness and maintenance · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Review security for production readiness across the current project state.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Review authentication, authorization, sessions/cookies, input validation, file uploads, redirects, dependency risk, admin surfaces, secrets handling, logging, and error exposure against OWASP and the 8 security domains.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Strict security posture: describe sensitive surfaces only by variable name, command, path, or risk type; never expose secrets, `.env` values, tokens, or credentials.

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-4.6. Next: MOS-6.7. Recommended: MOS-6.7.
