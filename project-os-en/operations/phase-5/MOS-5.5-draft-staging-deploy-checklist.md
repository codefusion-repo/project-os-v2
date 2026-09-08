# MOS-5.5 — Draft staging deploy checklist

MOSDLC operation `draft-staging-deploy-checklist` · Phase 5 — Local, staging, and production deployment · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- PM approval: No (draft-only; the Human PM decides and runs the bundle)

**Does:** Draft the human staging deployment checklist naming variables and steps, never secret values.
**For:** To guide the human steps of the staging deployment.
**How:** Consume MOS-R.11 human gaps for the same unit, ref, and
`staging` environment. Retain still-valid results with their sources
and draft only pending checks or those needing renewal; never omit
required QA or human acceptance. Name variables, never secrets.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Strict security posture: describe sensitive surfaces only by variable name, command, path, or risk type; never expose secrets, `.env` values, tokens, or credentials.
- Depend on the target adapter's `Project-specific notes`: use only target-owned commands and paths documented there; fail closed if they are missing or ambiguous.

**Deliver:** output.status_result. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-5.4. Next: MOS-5.6. Recommended: MOS-5.6.
