# MOS-5.7 — Analyze production deploy readiness

MOSDLC operation `analyze-production-deploy-readiness` · Phase 5 — Local, staging, and production deployment · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- PM approval: No (read-only)

**Does:** Analyze production deployment readiness from target-owned notes and repository evidence without configuring production or deploying anything.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Identify production prerequisites, missing target-owned notes, approval/change-window expectations, rollback and monitoring readiness, payment/auth/config risk types, smoke-check expectations, and secret/config risk types.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Strict security posture: describe sensitive surfaces only by variable name, command, path, or risk type; never expose secrets, `.env` values, tokens, or credentials.
- Depend on the target adapter's `Project-specific notes`: use only target-owned commands and paths documented there; fail closed if they are missing or ambiguous.

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.13. Next: MOS-5.8, MOS-5.14. Recommended: MOS-5.8.
