# MOS-6.3 analyze-performance-improvements

MOSDLC:
  ID: MOS-6.3
  Phase: Fase 6 - Maintenance and tooling
  Surface: actor.browser_chat
  Compatibility source: none
  Classification: new
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state

OPERATION:
  Analyze and recommend performance improvements.
  Source map summary: Analiza y recomienda mejoras de rendimiento. Priorizar optimizaciones con evidencia. Análisis read-only con recomendaciones accionables.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PATH_SCOPE=<PATH_SCOPE>   # optional
  FOCUS=<FOCUS>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only and emit only the declared output contracts.
  Apply boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  This is a new MOSDLC operation with no direct 00-37 compatibility source.
  Do not delete, rename, renumber, or bypass any 00-37 compatibility template.

LIVE_STATE:
  Read TARGET_REPOSITORY code, hot paths, and any existing performance notes live.
  If PATH_SCOPE or FOCUS is provided, restrict inspection to that requested area unless evidence shows the scope is insufficient.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Identify evidence-backed performance risks such as inefficient algorithms, unnecessary I/O, redundant computation, or missing caching.
  Recommend improvements with concrete file or line references and expected impact.
  Prioritize recommendations by estimated impact versus effort.
  Return status.needs_context when TARGET_REPOSITORY evidence cannot be inspected.
  Do not apply optimizations, edit files, run profilers against production, or claim performance is validated.

OUTPUT:
  output.status_result carrying the performance findings, recommendations, priority, and safe recommended next operation.

LIMITS:
  Read-only performance analysis; no repository, GitHub, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-6.9.
