# MOS-5.13 — Execute staging deploy

MOSDLC operation `execute-staging-deploy` · Phase 5 — Local, staging, and production deployment · Risk: high.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: terminal_agent
- Kernel: workflow.deployment · mode.delegated_deploy_execution · output.execution_report
- Evidence: evidence.pm_approval, evidence.source_basis, evidence.target_adoption, evidence.deployment_readiness, evidence.validation_output, evidence.repo_state
- PM approval: Yes (exact for target, environment, and action; never implicit)

**Does:** Execute the deployment in staging by terminal agent only if the target supports it.
**For:** Deploy frictionless internal staging when safe.
**How:** Execute only target-owned commands under exact approval and report redacted.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Run only approved target-owned commands for staging, one environment at a time; never invent, guess, or broaden deployment commands.
- Require exact PM approval for target, environment, and action before each command; if a target-owned command, approval, readiness, adoption, or validation is missing, fail closed to `status.blocked`.
- Redact sensitive values as `[REDACTED]`; do not request secrets, dump the environment (`env`, `printenv`, `set`), or claim success without post-deploy validation.
- Strict security posture: describe sensitive surfaces only by variable name, command, path, or risk type; never expose secrets, `.env` values, tokens, or credentials.
- Internal-only (CodeFusion use): remove, hide, disable, or convert this operation before any public Project OS release.

**Deliver:** output.execution_report. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-5.12. Next: MOS-R.13. Recommended: MOS-R.13.
