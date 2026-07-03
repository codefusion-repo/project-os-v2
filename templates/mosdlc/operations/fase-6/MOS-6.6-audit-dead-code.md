# MOS-6.6 audit-dead-code

MOSDLC:
  ID: MOS-6.6
  Phase: Fase 6 - Maintenance and tooling
  Surface: actor.browser_chat
  Compatibility source: none
  Classification: new
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state

OPERATION:
  Audit for orphaned code, legacy code, unused variables, obsolete functions, and dead code.
  Source map summary: Analizar en busca de código huérfano, código legacy, variables sin uso, funciones obsoletas y código inútil. Reducir superficie muerta y deuda técnica. Auditoría read-only con evidencia de archivos y líneas.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PATH_SCOPE=<PATH_SCOPE>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only and emit only the declared output contracts.
  Apply boundary.implementation_discipline, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  This is a new MOSDLC operation with no direct 00-37 compatibility source.
  Do not delete, rename, renumber, or bypass any 00-37 compatibility template.

LIVE_STATE:
  Read TARGET_REPOSITORY code and its reference graph (imports, calls, exports) live.
  If PATH_SCOPE is provided, restrict inspection to that requested area unless evidence shows the scope is insufficient.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Identify orphaned modules, legacy code paths, unused variables, obsolete functions, and other dead code with concrete file and line evidence.
  Distinguish genuinely dead code from code that is unreferenced locally but part of a public or documented surface.
  Classify each finding by removal risk and confidence.
  Return status.needs_context when code evidence cannot be inspected.
  Do not delete or edit files, or claim dead-code removal is complete.

OUTPUT:
  output.status_result carrying the dead-code findings, file/line references, removal risk, and safe recommended next operation.

LIMITS:
  Read-only dead-code audit; no repository, GitHub, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-6.12.
