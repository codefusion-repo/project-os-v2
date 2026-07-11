# MOS-R.13 — Verify post deploy state

MOSDLC operation `verify-post-deploy-state` · Phase 5 — Local, staging, and production deployment · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.validation_output
- PM approval: No (read-only verification)

**Does:** Verify the post-deploy state of the target environment, read-only, and report redacted health evidence.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Read-only health and smoke verification for TARGET_ENVIRONMENT using only target-owned checks from Project-specific notes or repository documentation.

**Variables**
- Required: TARGET_ENVIRONMENT
- Optional: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Fail closed if the target lacks that environment or target-owned checks.
- Report endpoints by name plus check names and results; never environment values, tokens, or connection strings.
- Do not redeploy, restart services, edit configuration, or run corrections.

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-5.11, MOS-5.13, MOS-R.12. Next: MOS-R.14. Recommended: MOS-R.14.
