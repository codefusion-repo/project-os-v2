# MOS-5.1 analyze-local-deploy-readiness

MOSDLC:
  ID: MOS-5.1
  Phase: Fase 5 - Despliegue local / staging / produccion
  Surface: actor.browser_chat / actor.terminal_agent
  Compatibility source: none
  Classification: new; split-candidate (analisis vs configuracion); merge-candidate (via TARGET_ENVIRONMENT, ver MOS-R.11)
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis

OPERATION:
  Analyze local deployment readiness from target-owned notes and repository evidence without configuring or deploying anything.
  Source map summary: Analiza readiness y configuracion necesaria del despliegue local. Preparar un despliegue local seguro y reproducible. Analisis read-only desde target notes y repo; toda configuracion con escritura va por ruta delegada aprobada.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only and emit only the declared output contracts.
  Apply boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, boundary.validation_discipline, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  No 00-37 compatibility source is mapped for this Fase 5 operation.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read target adoption notes, Project-specific notes, local deploy docs, local config names, dependency notes, and relevant repository state live.
  Treat local readiness as analysis only; it does not authorize configuration changes, command execution, or deploy behavior.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Identify local-only prerequisites, missing target-owned notes, dependency/service assumptions, database or seed-data readiness, local validation expectations, and secret/config risk types.
  Refer to sensitive inputs only by file paths, variable names, command names, and risk types; redact values as [REDACTED].
  Return status.needs_context when target-owned local deploy notes or repository evidence are missing or ambiguous.
  Do not run local deploy commands, modify config, request secret values, inspect hidden values, run broad environment/config dumps such as env, printenv, set, framework config dumps, or CI secret-context dumps, or claim local deploy readiness is complete.

OUTPUT:
  output.status_result carrying the local readiness analysis, missing evidence, risk types, and safe recommended next operation.

LIMITS:
  Read-only/draft-only local deployment readiness analysis; no repository, GitHub, settings, runtime-config, secret-store, external-service, database, host, DNS, payment/auth, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-5.2.
