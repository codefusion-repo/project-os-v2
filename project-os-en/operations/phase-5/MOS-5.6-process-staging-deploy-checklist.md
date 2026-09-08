# MOS-5.6 — Process staging deploy checklist

MOSDLC operation `process-staging-deploy-checklist` · Phase 5 — Local, staging, and production deployment · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Process the result of the human steps for staging deployment.
**For:** To confirm readiness or derive gaps before continuing.
**How:** Compare CHECKLIST_RESULT with the checklist unit, ref, and
environment and apply MOS-R.11 without recapturing valid evidence. With
sufficient readiness, consume MOS-5.12 in this response; require no
further checklist or selection. Stale or failed results retain blockers;
correction or rollback disposition and approval follow their own routes.
Only an already executed deployment proceeds to MOS-R.13 verification.

**Variables**
- Required: CHECKLIST_RESULT
- Optional: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Strict security posture: describe sensitive surfaces only by variable name, command, path, or risk type; never expose secrets, `.env` values, tokens, or credentials.
- Depend on the target adapter's `Project-specific notes`: use only target-owned commands and paths documented there; fail closed if they are missing or ambiguous.

**Deliver:** output.status_result (+output.route_prompt, output.pm_command_bundle). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-5.5. Next: MOS-5.12 or MOS-R.13. Recommended: MOS-5.12.
