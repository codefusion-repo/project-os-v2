# MOS-R.15 draft-rollback-commands

MOSDLC:
  ID: MOS-R.15
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: none
  Classification: accepted-recommended; new
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.pm_command_bundle
  Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis

OPERATION:
  Draft rollback commands or a rollback route for a failed deployment, for Human PM execution only, using strictly target-owned rollback paths.
  Source map summary: Draftea comandos o ruta de rollback cuando un despliegue falla. Volver a un estado seguro sin improvisar bajo presión. Bundle copy-safe desde rutas de rollback target-owned.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  TARGET_ENVIRONMENT=<TARGET_ENVIRONMENT>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.copy_safe_commands, boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  No 00-37 compatibility source is mapped for this recommended operation.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  This operation depends on the target actually having target-owned rollback commands or documented rollback paths for TARGET_ENVIRONMENT in its Project-specific notes or deploy documentation; fail closed to status.needs_context when they do not exist.
  Treat the bundle as a Human PM-executed output.pm_command_bundle only; the template never executes it.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft only rollback commands that already exist in target-owned notes or repository deploy documentation; preserve exact command names and environment targets from evidence.
  Fail closed to status.needs_context when rollback paths are missing, conflicting, untested, or ambiguous; improvising a rollback under pressure is never a safe route.
  Keep scope, risk, data-loss warnings, secret-safety, and verification prose outside executable blocks and follow templates/pm-command-bundle.md.
  Redact sensitive values as [REDACTED] and reference only variable names or risk types; never print environment values or request secrets.
  Do not execute the bundle, invent commands, change host/DNS/provider settings, or authorize rollback for any environment.

OUTPUT:
  output.pm_command_bundle for Human PM-executed rollback commands, or a fail-closed status when evidence is insufficient.

LIMITS:
  Command drafting only; the Human PM decides and executes any rollback command after separate exact approval per target, environment, and action.
  Internal-only exposure: this operation must be removed, hidden, disabled, or converted before any public release of the operating catalog (pre-release convert).
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  Human PM execution of the bundle; then MOS-R.16.
