# MOS-5.8 — Draft production deploy checklist

MOSDLC operation `draft-production-deploy-checklist` · Phase 5 — Local, staging, and production deployment · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- PM approval: No (draft-only; the Human PM decides and runs the bundle)

**Does:** Draft a Human PM-facing production deployment checklist that names required production variables, approvals, verification steps, rollback awareness, and human steps without exposing values.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft production human steps for approval confirmation, change-window readiness, environment and variable-name checks, host/DNS/provider awareness, smoke checks, monitoring checks, rollback awareness, and post-deploy verification routing when target-owned notes support them.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Strict security posture: describe sensitive surfaces only by variable name, command, path, or risk type; never expose secrets, `.env` values, tokens, or credentials.
- Depend on the target adapter's `Project-specific notes`: use only target-owned commands and paths documented there; fail closed if they are missing or ambiguous.

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-5.7. Next: MOS-5.9. Recommended: MOS-5.9.
