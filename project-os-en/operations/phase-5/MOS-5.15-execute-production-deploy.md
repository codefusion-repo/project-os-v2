# MOS-5.15 — Production deploy (Human PM)

MOSDLC operation `execute-production-deploy` · Phase 5 — Local, staging, and production deployment · Risk: high.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: human_pm
- Kernel: workflow and mode remain candidates, not applied (production is not agent-executed; Human PM by default) · output.execution_report
- Evidence: evidence.pm_approval, evidence.source_basis, evidence.target_adoption, evidence.deployment_readiness, evidence.validation_output, evidence.repo_state, evidence.exact_ref
- PM approval: Yes (exact for target, environment, and action; never implicit)

**Does:** Human PM executes the production deployment prepared in MOS-5.14.
**For:** To complete the same outcome in production under human control.
**How:** PM verifies target, exact ref, production readiness, required human
checks, validation, rollback, and exact approval for that action before running
target-owned commands. Retain the unit and applicable evidence under the common
contract; staging PASS and its approval do not satisfy the production gate. The
agent only prepares evidence/drafts or verifies read-only under existing
workflows; it does not execute production even if the target has commands.
Verify the human execution result through MOS-R.13 before claiming success.

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
