# MOS-5.6 process-staging-deploy-checklist

MOSDLC:
  ID: MOS-5.6
  Phase: Fase 5 - Despliegue local / staging / produccion
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: none
  Classification: new
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.status_result, output.route_prompt, output.pm_command_bundle
  Evidence: evidence.source_basis, evidence.repo_state

OPERATION:
  Classify Human PM staging deployment checklist results into continue, correction, follow-up, no-op, or PM decision paths without mutating repository, GitHub, or environment state.
  Source map summary: Procesa el resultado de los pasos humanos del despliegue staging. Confirmar readiness o derivar gaps antes de continuar. Clasifica CHECKLIST_RESULT hacia continuar, corregir o detener.

INPUT:
  CHECKLIST_RESULT=<CHECKLIST_RESULT>
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.copy_safe_commands, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  No 00-37 compatibility source is mapped for this Fase 5 operation.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read CHECKLIST_RESULT, staging checklist source, target repository evidence, and PM decisions live.
  Treat the result as classification input only; this template does not verify staging deployment by executing commands.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Classify CHECKLIST_RESULT as continue, correction, follow-up, no-op, or PM decision only when evidence supports that route.
  For continue, recommend MOS-5.12 only when target-owned staging deploy commands are expected to exist; otherwise recommend Human PM execution or status.needs_context.
  Draft output.route_prompt only for scoped correction work and state that route prompts are non-authorizing outputs.
  Draft output.pm_command_bundle only for Human PM-executed follow-ups or command drafting; do not include deploy commands unless target-owned evidence already provides them.
  Redact sensitive values as [REDACTED] and report only variable names, file paths, command names, and risk types.
  Do not execute deployment, mutate GitHub, edit files, change host/DNS/provider settings, request secrets, expose values, run broad environment/config dumps, or invent staging deploy commands.

OUTPUT:
  output.status_result plus output.route_prompt or output.pm_command_bundle only when checklist classification selects that draft path.

LIMITS:
  Draft-only/read-only staging checklist classification; no deployment behavior and no repository, GitHub, runtime-config, secret-store, host, DNS, provider, or external-service mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-5.12 when target-owned command evidence exists; otherwise MOS-R.13 after Human PM staging deployment or MOS-R.3 for a PM decision.
