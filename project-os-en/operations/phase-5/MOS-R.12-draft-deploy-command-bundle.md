# MOS-R.12 — Draft deploy command bundle

MOSDLC operation `draft-deploy-command-bundle` · Phase 5 — Local, staging, and production deployment · Risk: high.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis, evidence.deployment_readiness, evidence.validation_output, evidence.exact_ref
- PM approval: No for drafting; execution requires exact approval for target, environment, and action

**Does:** Draft a copy-safe bundle of deployment commands for an environment.
**For:** To unify drafting by environment without losing PM clarity.
**How:** Consume sufficient MOS-R.11 readiness for the same unit, target,
exact ref, and environment. A direct entry reconstructs that evidence; it does
not require another readiness invocation if still current. Apply common
evidence reuse and `project-os-en/templates/pm-command-bundle.md` formatting:
reviewed target-owned commands, gate/responsible party, renewed/reused evidence,
risk, rollback, and postconditions outside executable blocks.

The draft identifies current or pending exact approval for that target,
environment, action, and ref; neither target capability nor readiness is
permission. Do not combine configuration, release, several environments, or
rollback in an executable chain with pending gates. Missing material evidence
fails closed. Local/staging may proceed to MOS-5.11/MOS-5.13 only under their own
delegated authorization and resolution; production stays in MOS-5.15 for Human PM.
MOS-5.10/5.12/5.14 are entries delegating here; do not invoke them again from this
bundle. Subsequent MOS-R.13 verification retains the unit and is required
after execution.

**Variables**
- Required: TARGET_REPOSITORY, TARGET_ENVIRONMENT
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Do not invent commands or run the bundle; the Human PM decides and executes.
- Redact secrets as `[REDACTED]`; do not request values or dump environment/configuration.
- Internal-only/pre-release-convert: remove, hide, disable, or convert before any public release of the operation catalog.

**Deliver:** output.pm_command_bundle. For missing, ambiguous or secret-sensitive commands without redaction, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.11. Next: PM execution of the bundle or the environment execution operation with exact approval; then MOS-R.13. Recommended: MOS-R.13 after running.
