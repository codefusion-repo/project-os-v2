# MOS-5.14 — Draft production deploy commands

MOSDLC operation `draft-production-deploy-commands` · Phase 5 — Local, staging, and production deployment · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- PM approval: No (draft-only; the Human PM decides and runs the bundle)

**Does:** Draft a production deployment command bundle for Human PM execution only, using strictly target-owned production deploy commands.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft only commands that already exist in target-owned notes or repository deploy documentation; preserve exact command names and production targets from evidence.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Strict security posture: describe sensitive surfaces only by variable name, command, path, or risk type; never expose secrets, `.env` values, tokens, or credentials.
- Depend on the target adapter's `Project-specific notes`: use only target-owned commands and paths documented there; fail closed if they are missing or ambiguous.
- Internal-only (CodeFusion use): remove, hide, disable, or convert this operation before any public Project OS release.

**Deliver:** output.pm_command_bundle. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-5.9. Next: MOS-5.15. Recommended: none.
