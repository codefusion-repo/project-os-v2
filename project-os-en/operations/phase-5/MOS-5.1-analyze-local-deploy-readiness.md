# MOS-5.1 — Analyze local deploy readiness

MOSDLC operation `analyze-local-deploy-readiness` · Phase 5 — Local, staging, and production deployment · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- PM approval: No (read-only)

**Does:** Analyze the readiness and required configuration of the local deployment.
**For:** To prepare a secure and reproducible local deployment.
**How:** Perform a read-only review of target notes and the repository; every configuration write goes through an approved delegated route.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Strict security posture: describe sensitive surfaces only by variable name, command, path, or risk type; never expose secrets, `.env` values, tokens, or credentials.
- Depend on the target adapter's `Project-specific notes`: use only target-owned commands and paths documented there; fail closed if they are missing or ambiguous.

**Deliver:** output.status_result. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-4.6. Next: MOS-5.2, MOS-5.10. Recommended: MOS-5.2.
