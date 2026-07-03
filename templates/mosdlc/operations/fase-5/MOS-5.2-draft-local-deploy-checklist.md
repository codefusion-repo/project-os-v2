# MOS-5.2 draft-local-deploy-checklist

MOSDLC:
  ID: MOS-5.2
  Phase: Fase 5 - Despliegue local / staging / produccion
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: none
  Classification: new
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis

OPERATION:
  Draft a Human PM-facing local deployment checklist that names required local variables and human steps without exposing values.
  Source map summary: Draftea el checklist humano de despliegue local nombrando variables y pasos, nunca valores secretos. Guiar pasos humanos del despliegue local. Checklist copy-safe para el Humano PM; secretos solo como nombres de variable.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  No 00-37 compatibility source is mapped for this Fase 5 operation.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read target-owned local deployment notes, adoption notes, repository docs, local dependency notes, and prior MOS-5.1 readiness findings live.
  Treat the checklist as Human PM guidance only; the template does not perform or verify any local deployment step.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft local human steps for dependency setup, local service availability, database readiness, variable-name checks, validation/smoke checks, and rollback or cleanup awareness when target-owned notes support them.
  Name sensitive configuration by variable name or risk type only; values stay [REDACTED] and must never be requested or displayed.
  Fail closed to status.needs_context when target-owned notes do not identify enough local steps for a copy-safe checklist.
  Do not execute commands, edit files, mutate GitHub, change local config, run broad environment/config dumps, or invent local deploy steps.

OUTPUT:
  output.status_result carrying the drafted local deployment checklist or the fail-closed status.

LIMITS:
  Checklist drafting only; Human PM decides and performs any local setup or deploy step.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-5.3.
