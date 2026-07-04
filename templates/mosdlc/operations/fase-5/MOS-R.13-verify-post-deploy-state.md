# MOS-R.13 verify-post-deploy-state

MOSDLC:
  ID: MOS-R.13
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat / actor.terminal_agent
  Compatibility source: templates/operations/11-verify-post-merge-state.md
  Classification: accepted-recommended; new
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state, evidence.validation_output

OPERATION:
  Verify the post-deploy state of the target environment, read-only, and report redacted health evidence.
  Source map summary: Verifica el estado post-deploy del entorno objetivo. Confirmar que el despliegue quedó saludable. Chequeo read-only de salud y humo; reporta redactado.

INPUT:
  TARGET_ENVIRONMENT=<TARGET_ENVIRONMENT>
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/11-verify-post-merge-state.md as compatibility source for this recommended operation shape.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  This operation depends on the target actually having the TARGET_ENVIRONMENT deployment surface and target-owned health or smoke checks; fail closed to status.needs_context when they do not exist.
  Read deployment evidence live at execution time; treat the deploy report as a claim until health evidence confirms it.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Read-only health and smoke verification for TARGET_ENVIRONMENT using only target-owned checks from Project-specific notes or repository documentation.
  Redact sensitive or secret-looking values as [REDACTED]; report only endpoints by name, check names, and outcome summaries, and never print environment values, secrets, tokens, or connection strings.
  Return status.needs_context when the environment or its checks cannot be read, and status.blocked when verification evidence suggests an unhealthy deploy needing PM attention.
  Do not redeploy, restart services, edit configuration, or execute corrective commands.

OUTPUT:
  output.status_result with the redacted post-deploy verification evidence and a clear healthy/unhealthy assessment.

LIMITS:
  Read-only verification; deployment result processing and any corrective action are separate operations with their own gates.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-R.14.
