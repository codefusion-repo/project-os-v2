# MOS-3.23 — Request security review

MOSDLC operation `request-security-review` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → external_recipient
- Kernel: workflow.security_revision · mode.review_only · output.security_review_prompt
- Evidence: evidence.repo_state, evidence.source_basis
- PM approval: No (the route prompt does not authorize; writing requires exact PM approval)

**Does:** Draft the OWASP security review prompt and the 8 domains where appropriate.
**For:** Obtain an external security gate with mandatory redaction.
**How:** Prompt with sensitive surface described without exposing secrets.

**Variables**
- Required: PR_NUMBER
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Strict security posture: describe sensitive surfaces only by variable name, command, path, or risk type; never expose secrets, `.env` values, tokens, or credentials.

**Deliver:** output.security_review_prompt. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.7 or MOS-6.1. Next: MOS-3.25 when the result arrives. Recommended: MOS-3.25.
