# MOS-R.13 — Verify post deploy state

MOSDLC operation `verify-post-deploy-state` · Phase 5 — Local, staging, and production deployment · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.validation_output
- PM approval: No (read-only verification)

**Does:** Checks the post-deploy status of the target environment.
**For:** Confirm that the deployment was healthy with evidence of health or smoke.
**How:** Use only target-owned checks and report redacted evidence.

**Variables**
- Required: TARGET_ENVIRONMENT
- Optional: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Fail closed if the target lacks that environment or target-owned checks.
- Report endpoints by name plus check names and results; never environment values, tokens, or connection strings.
- Do not redeploy, restart services, edit configuration, or run corrections.

**Deliver:** output.status_result. For unreadable checks, return `status.needs_context`; if the deployment is unhealthy, return `status.blocked`.

**Connections:** Previously: MOS-5.11, MOS-5.13, PM run of MOS-R.12 or approved deployment. Next: MOS-R.14. Recommended: MOS-R.14.
