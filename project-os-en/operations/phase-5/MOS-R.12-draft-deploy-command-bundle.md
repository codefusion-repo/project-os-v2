# MOS-R.12 — Draft deploy command bundle

MOSDLC operation `draft-deploy-command-bundle` · Phase 5 — Local, staging, and production deployment · Risk: high.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- PM approval: No for drafting; execution requires exact approval for target, environment, and action

**Does:** Draft a copy-safe bundle of deployment commands for an environment.
**For:** Unify drafting by environment without losing PM clarity.
**How:** Use only target-owned commands and keep risk, rollback, and verification out of executable blocks.

**Variables**
- Required: TARGET_REPOSITORY, TARGET_ENVIRONMENT
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Do not invent commands or run the bundle; the Human PM decides and executes.
- Redact secrets as `[REDACTED]`; do not request values or dump environment/configuration.
- Internal-only/pre-release-convert: remove, hide, disable, or convert before any public release of the operation catalog.

**Deliver:** output.pm_command_bundle. For missing, ambiguous or secret-sensitive commands without redaction, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.11. Next: PM execution of the bundle or the environment execution operation with exact approval; then MOS-R.13. Recommended: MOS-R.13 after running.
