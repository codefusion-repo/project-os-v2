# MOS-R.15 — Draft rollback commands

MOSDLC operation `draft-rollback-commands` · Phase 5 — Local, staging, and production deployment · Risk: high.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- PM approval: No for drafting; rollback requires exact approval for target, environment, and action

**Does:** Draft commands or rollback path for a failed deployment.
**For:** To return to a safe state without improvising under pressure.
**How:** Use only target-owned rollback paths and keep warnings outside of executable blocks.

**Variables**
- Required: TARGET_REPOSITORY, TARGET_ENVIRONMENT
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Do not invent commands or run rollback; fail closed when the route is missing, conflicting, untested, or ambiguous.
- Redact secrets; never print environment values or request credentials.
- Internal-only/pre-release-convert: remove, hide, disable, or convert before any public release of the operation catalog.

**Deliver:** output.pm_command_bundle. In case of insufficient rollback paths or missing approval for execution, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.14 with rollback chosen. Next: PM execution of the bundle; then MOS-R.16. Recommended: MOS-R.16 after running.
