# MOS-3.23 — Request security review

MOSDLC operation `request-security-review` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → external_recipient
- Kernel: workflow.security_revision · mode.review_only · output.security_review_prompt
- Evidence: evidence.repo_state, evidence.source_basis
- PM approval: No (the route prompt does not authorize; writing requires exact PM approval)

**Does:** Draft an external-recipient security review prompt with strict secret-redaction posture.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft output.security_review_prompt with review objective, sensitive surfaces, OWASP areas, the eight security domains where relevant, evidence to inspect, findings format, and redaction rules.

**Variables**
- Required: PR_NUMBER
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Strict security posture: describe sensitive surfaces only by variable name, command, path, or risk type; never expose secrets, `.env` values, tokens, or credentials.

**Deliver:** output.security_review_prompt. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.7, MOS-6.1. Next: MOS-3.25. Recommended: MOS-3.25.
