# MOS-5.5 draft-staging-deploy-checklist

MOSDLC:
  ID: MOS-5.5
  Phase: Fase 5 - Despliegue local / staging / produccion
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: none
  Classification: new
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis

OPERATION:
  Draft a Human PM-facing staging deployment checklist that names required staging variables, host/DNS checks, dashboard checks, and human steps without exposing values.
  Source map summary: Draftea el checklist humano de despliegue staging nombrando variables y pasos, nunca valores secretos. Guiar pasos humanos del despliegue staging. Checklist copy-safe para el Humano PM; secretos solo como nombres de variable.

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
  Read target-owned staging deployment notes, adoption notes, repository docs, host/DNS notes, dashboard notes, and prior MOS-5.4 readiness findings live.
  Treat the checklist as Human PM guidance only; the template does not perform or verify any staging deployment step.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft staging human steps for environment selection, host and DNS review, external dashboard review, CI/provider variable-name checks, smoke checks, monitoring awareness, and rollback awareness when target-owned notes support them.
  Name sensitive configuration by variable name or risk type only; values stay [REDACTED] and must never be requested or displayed.
  Fail closed to status.needs_context when target-owned notes do not identify enough staging steps for a copy-safe checklist.
  Do not execute commands, edit files, mutate GitHub, change host/DNS/provider settings, run broad environment/config dumps, or invent staging deploy steps.

OUTPUT:
  output.status_result carrying the drafted staging deployment checklist or the fail-closed status.

LIMITS:
  Checklist drafting only; Human PM decides and performs any staging setup or deploy step.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-5.6.
