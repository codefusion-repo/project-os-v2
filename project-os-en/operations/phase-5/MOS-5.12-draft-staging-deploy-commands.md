# MOS-5.12 — Draft staging deploy commands

MOSDLC operation `draft-staging-deploy-commands` · Phase 5 — Local, staging, and production deployment · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- PM approval: No (draft-only; the Human PM decides and runs the bundle)

**Does:** Draft the bundle of staging deployment commands from the target-owned commands in Project-specific notes.
**For:** To prepare the execution of the staging deployment without inventing commands.
**How:** Build a copy-safe bundle only from target-owned commands; never print secrets.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Strict security posture: describe sensitive surfaces only by variable name, command, path, or risk type; never expose secrets, `.env` values, tokens, or credentials.
- Depend on the target adapter's `Project-specific notes`: use only target-owned commands and paths documented there; fail closed if they are missing or ambiguous.
- Internal-only (CodeFusion use): remove, hide, disable, or convert this operation before any public Project OS release.

**Deliver:** output.pm_command_bundle. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-5.6. Next: MOS-5.13 or execution of the Human PM. Recommended: MOS-5.13 only with exact approval.
