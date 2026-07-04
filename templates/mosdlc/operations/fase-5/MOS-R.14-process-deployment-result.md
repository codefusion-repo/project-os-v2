# MOS-R.14 process-deployment-result

MOSDLC:
  ID: MOS-R.14
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: none
  Classification: accepted-recommended; new
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.status_result, output.route_prompt, output.pm_command_bundle
  Evidence: evidence.source_basis, evidence.repo_state

OPERATION:
  Process a deployment result (success, partial, or failure) into a safe continue, correct, or rollback route, draft-only.
  Source map summary: Procesa el resultado de un despliegue (éxito, parcial o fallo). Decidir continuar, corregir o hacer rollback con evidencia. Clasifica DEPLOYMENT_RESULT hacia siguiente fase, corrección o rollback.

INPUT:
  DEPLOYMENT_RESULT=<DEPLOYMENT_RESULT>
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
  Read DEPLOYMENT_RESULT and the MOS-R.13 verification evidence live; treat the reported result as a claim until verification evidence supports it.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Classify DEPLOYMENT_RESULT as continue (healthy), scoped correction, or rollback candidate only when evidence supports that route.
  Draft output.route_prompt only for scoped corrections as a non-authorizing output, and output.pm_command_bundle only for Human PM-executed follow-up actions.
  Return status.needs_context when the result or its verification evidence cannot be inspected, and status.needs_pm_decision when continue-versus-rollback requires an explicit PM choice.
  Redact sensitive or secret-looking values from deploy output as [REDACTED]; report only command names, check names, and risk types, and never request secrets.
  Do not deploy, roll back, execute corrections, or authorize any environment action.

OUTPUT:
  output.status_result with the classification and evidence, plus output.route_prompt or output.pm_command_bundle only when the classification selects that draft path.

LIMITS:
  Draft-only classification; route prompts are non-authorizing outputs and command bundles are Human PM-executed only.
  Rollback is never automatic: the PM decision selects it, and rollback drafting stays in MOS-R.15 with its own gates.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-R.15 when the deploy failed and the PM chooses rollback; MOS-3.3 for follow-ups.
