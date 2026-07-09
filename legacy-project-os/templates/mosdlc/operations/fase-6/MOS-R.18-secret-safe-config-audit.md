# MOS-R.18 secret-safe-config-audit

MOSDLC:
  ID: MOS-R.18
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat / actor.terminal_agent
  Compatibility source: none
  Classification: accepted-recommended; new
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state

OPERATION:
  Audit environment and configuration risk for the target project reporting only file paths, variable names, and risk types, never values.
  Source map summary: Audita entorno/config reportando solo rutas de archivo, nombres de variable y tipo de riesgo; nunca valores. Detectar riesgos de configuración sin exponer secretos. Escaneo redactado por diseño; valores siempre como [REDACTED].

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  No 00-37 compatibility source is mapped for this recommended operation.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read the target repository's configuration surfaces (env templates, config files, CI configuration) live at execution time; never open or quote secret stores.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Read-only, redacted-by-design scan of environment and configuration risk: committed secrets, secret-looking values, unsafe defaults, missing env templates, and overexposed configuration.
  Report every finding as file path plus variable name plus risk type; render any value as [REDACTED] with no partial quoting, prefixes, or lengths that could reconstruct it.
  Do not run broad environment/config dumps such as env, printenv, set, framework config dumps, or CI secret-context dumps.
  Return status.needs_context when configuration surfaces cannot be read, and status.blocked when a live exposed secret needs immediate PM attention.
  Do not rotate keys, edit configuration, modify secret stores, or touch deployment secrets.

OUTPUT:
  output.status_result with the redacted findings list (path, variable name, risk type) and the recommended follow-up per risk.

LIMITS:
  Read-only audit that never exposes, requests, quotes, summarizes, or invents secret values.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.3 per detected risk.
