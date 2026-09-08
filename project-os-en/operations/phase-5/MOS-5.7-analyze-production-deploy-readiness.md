# MOS-5.7 — Analyze production deploy readiness

MOSDLC operation `analyze-production-deploy-readiness` · Phase 5 — Local, staging, and production deployment · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- PM approval: No (read-only)

**Does:** Analyze the readiness and required configuration of the production deployment.
**For:** To prepare a secure and reproducible production deployment.
**How:** Delegate review to MOS-R.11 with `TARGET_ENVIRONMENT=production`
and already reconstructed live relations; apply its evidence and gates.
Only pending human checks consume MOS-5.8; sufficient readiness
consumes MOS-5.14 in the same response without recapture. Every
configuration write retains its own approval and limits.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Strict security posture: describe sensitive surfaces only by variable name, command, path, or risk type; never expose secrets, `.env` values, tokens, or credentials.
- Depend on the target adapter's `Project-specific notes`: use only target-owned commands and paths documented there; fail closed if they are missing or ambiguous.

**Deliver:** output.status_result. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: QA/release or prior environment when required by the target. Next: MOS-5.8 only for pending human checks; MOS-5.14 with sufficient readiness. Recommended: the safe output resolved by MOS-R.11, without another selection.
