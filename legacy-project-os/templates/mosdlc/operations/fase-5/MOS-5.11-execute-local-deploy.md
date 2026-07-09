# MOS-5.11 execute-local-deploy

MOSDLC:
  ID: MOS-5.11
  Phase: Fase 5 - Despliegue local / staging / produccion
  Surface: actor.terminal_agent
  Compatibility source: none
  Classification: new
  Workflow: workflow.deployment
  Mode: mode.delegated_deploy_execution
  Output: output.execution_report
  Evidence: evidence.pm_approval, evidence.source_basis, evidence.target_adoption, evidence.deployment_readiness, evidence.validation_output, evidence.repo_state

OPERATION:
  Execute an internal local/debug deployment through workflow.deployment and mode.delegated_deploy_execution, running only target-owned commands for the one approved local environment and failing closed otherwise.
  Source map summary: Ejecuta despliegue local/debug por terminal agent solo si el target lo soporta. Ejecuta solo comandos target-owned bajo aprobacion exacta por target, entorno y accion, y reporta redactado. Internal-only; nunca public-safe por defecto.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Resolve workflow.deployment with mode.delegated_deploy_execution for actor.terminal_agent; both are internal-only and terminal-only, and production is never executed by this mode.
  Require exact PM approval scoped to target repository, environment (local), and action before any command. Emit output.execution_report.
  Apply boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, boundary.separate_pm_approval, and boundary.validation_discipline.

COMPATIBILITY_SOURCE:
  No 00-37 compatibility source is mapped for this Fase 5 operation.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read the target-owned local deploy commands from the target's Project-specific notes, exact PM approval evidence, adoption state, source basis, deployment readiness, and validation evidence live before running anything.
  Never invent, guess, or broaden deploy commands; use only documented target-owned commands for the approved local environment.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Fail closed to status.blocked when target-owned commands, exact environment-scoped approval, deployment readiness, adoption, source basis, validation, or secret-safety is missing or ambiguous.
  Run only the approved target-owned local deploy commands, one environment at a time; then verify post-deploy state and report redacted.
  Redact sensitive values as [REDACTED] and reference only variable names, command names, file paths, and risk types.
  Do not request secrets, print environment values, mutate config outside target-owned commands, or mutate GitHub.
  Do not run broad environment/config dumps such as env, printenv, or set, and do not claim local deploy success without validation.

OUTPUT:
  output.execution_report stating the approved local deploy result with evidence reviewed, values redacted, and the safe next step.

LIMITS:
  Internal-only, target-owned, exact-approval, fail-closed deploy execution for the local environment only; no repository, GitHub, secret-store, database, host, DNS, provider, payment/auth, or external-service mutation outside documented target-owned commands.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-R.13 after the local deployment; otherwise MOS-5.10 or MOS-R.3.
