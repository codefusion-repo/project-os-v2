# MOS-6.4 analyze-product-improvements

MOSDLC:
  ID: MOS-6.4
  Phase: Fase 6 - Maintenance and tooling
  Surface: actor.browser_chat
  Compatibility source: none
  Classification: new
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state

OPERATION:
  Analyze and recommend product improvements.
  Source map summary: Analiza y recomienda mejoras de producto. Alimentar el roadmap con mejoras fundadas. Análisis read-only de producto contra uso y docs.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
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
  Read TARGET_REPOSITORY product docs, requirements, roadmap, and observable product behavior live.
  Treat findings as advisory input to a future roadmap decision, not a roadmap change.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Identify evidence-backed product improvement opportunities from usage patterns, documented requirements, and known gaps.
  Recommend improvements with concrete doc or evidence references.
  Return status.needs_context when product docs or repository evidence cannot be inspected.
  Do not edit the roadmap, create issues, edit files, or claim a product decision has been made.

OUTPUT:
  output.status_result carrying the product-improvement findings, recommendations, and safe recommended next operation.

LIMITS:
  Read-only product analysis; no repository, GitHub, or roadmap mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-6.10.
