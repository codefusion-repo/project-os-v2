# MOS-R.16 process-rollback-result

MOSDLC:
  ID: MOS-R.16
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: none
  Classification: accepted-recommended; new
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.status_result, output.route_prompt, output.pm_command_bundle
  Evidence: evidence.source_basis, evidence.repo_state

OPERATION:
  Process the result of an executed rollback into incident, correction, or closure routes, draft-only, preserving traceability.
  Source map summary: Procesa el resultado de un rollback ejecutado. Cerrar el incidente de despliegue con trazabilidad. Clasifica ROLLBACK_RESULT hacia incidente, corrección o cierre.

INPUT:
  ROLLBACK_RESULT=<ROLLBACK_RESULT>
  TARGET_ENVIRONMENT=<TARGET_ENVIRONMENT>
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  No 00-37 compatibility source is mapped for this recommended operation.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read ROLLBACK_RESULT and post-rollback verification evidence live; treat the reported result as a claim until verification evidence supports it.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Classify ROLLBACK_RESULT as restored (safe state confirmed), partially restored, or failed only when evidence supports that route.
  Draft output.route_prompt only for scoped corrections as a non-authorizing output, and output.pm_command_bundle only for Human PM-executed follow-up actions such as incident issue creation.
  Return status.needs_context when the rollback evidence cannot be inspected, status.needs_pm_decision when the next route requires an explicit PM choice, and status.blocked when the environment remains unsafe.
  Redact sensitive or secret-looking values from rollback output as [REDACTED]; report only command names, check names, and risk types, and never request secrets.
  Do not redeploy, re-roll back, execute corrections, or authorize any environment action.

OUTPUT:
  output.status_result with the classification and evidence, plus output.route_prompt or output.pm_command_bundle only when the classification selects that draft path.

LIMITS:
  Draft-only classification; route prompts are non-authorizing outputs and command bundles are Human PM-executed only.
  Closing the deployment incident is a PM decision informed by this classification, never an automatic transition.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-R.8 when the rollback exposes an incident to process; MOS-3.3 for follow-ups.
