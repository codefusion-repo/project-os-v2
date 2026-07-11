# MOS-5.15 — Execute production deploy

MOSDLC operation `execute-production-deploy` · Phase 5 — Local, staging, and production deployment · Risk: high.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: terminal_agent
- Kernel: workflow and mode remain candidates, not applied (production is not agent-executed; Human PM by default) · output.execution_report
- Evidence: evidence.pm_approval, evidence.source_basis, evidence.target_adoption, evidence.validation_output, evidence.repo_state
- PM approval: Yes (exact for target, environment, and action; never implicit)

**Does:** Execute the deployment in production by terminal agent only if the target supports it.
**For:** Cover the internal case where the PM explicitly delegates production.
**How:** Execute only target-owned commands under exact approval and report redacted; By default production remains with the Human PM.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Production stays with the Human PM by default: the agent does not run this operation; only the Human PM runs commands drafted in MOS-5.14.
- Workflow and mode remain kernel candidates: do not add new kernel IDs without a proven strict gap and separate exact PM approval.
- Strict security posture: describe sensitive surfaces only by variable name, command, path, or risk type; never expose secrets, `.env` values, tokens, or credentials.
- Internal-only (CodeFusion use): remove, hide, disable, or convert this operation before any public Project OS release.

**Deliver:** output.execution_report. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-5.14. Next: MOS-R.13. Recommended: MOS-R.13.
