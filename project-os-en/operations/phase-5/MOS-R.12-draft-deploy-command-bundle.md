# MOS-R.12 — Draft deploy command bundle

MOSDLC operation `draft-deploy-command-bundle` · Phase 5 — Local, staging, and production deployment · Risk: high.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- PM approval: No for drafting; execution requires exact approval for target, environment, and action

**Does:** Draft the deployment command bundle for one environment selected by TARGET_ENVIRONMENT, for Human PM execution only, using strictly target-owned deploy commands.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft only commands that already exist in target-owned notes or repository deploy documentation; preserve exact command names and environment targets from evidence.

**Variables**
- Required: TARGET_REPOSITORY, TARGET_ENVIRONMENT
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Do not invent commands or run the bundle; the Human PM decides and executes.
- Redact secrets as `[REDACTED]`; do not request values or dump environment/configuration.
- Internal-only/pre-release-convert: remove, hide, disable, or convert before any public release of the operation catalog.

**Deliver:** output.pm_command_bundle. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.11. Next: MOS-R.13. Recommended: MOS-R.13.
