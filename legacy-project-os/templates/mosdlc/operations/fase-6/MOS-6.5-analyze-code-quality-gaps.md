# MOS-6.5 analyze-code-quality-gaps

MOSDLC:
  ID: MOS-6.5
  Phase: Fase 6 - Maintenance and tooling
  Surface: actor.browser_chat
  Compatibility source: templates/operations/25-audit-implementation-discipline-gaps.md
  Classification: new
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state

OPERATION:
  Analyze and recommend code normalization improvements or clean-code gaps.
  Source map summary: Analiza y recomienda mejoras de normalización de código o gaps de clean code. Mantener el código consistente con los estándares de la Fase 2. Análisis read-only contra estándares documentados.

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
  Use templates/operations/25-audit-implementation-discipline-gaps.md as compatibility source for this Fase 6 operation shape.
  Do not delete, rename, renumber, or bypass the 25 compatibility template.

LIVE_STATE:
  Read TARGET_REPOSITORY code and the documented Fase 2 coding-standards docs live.
  If PATH_SCOPE is provided, restrict inspection to that requested area unless evidence shows the scope is insufficient.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Inspect codebase structure and selected files for evidence-backed normalization and clean-code gaps.
  Map every finding to boundary.implementation_discipline and the documented coding-standards docs, not to a separate style guide.
  Classify each finding by severity or follow-up priority.
  Identify acceptable local tradeoffs and explicit project conventions as non-findings.
  Return status.needs_context when code or coding-standards evidence cannot be inspected.
  Do not refactor, edit files, commit, push, or claim normalization is complete.

OUTPUT:
  output.status_result carrying the code-quality findings, file/line references, severity, and safe recommended next operation.

LIMITS:
  Read-only code-quality analysis; no repository, GitHub, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-6.11.
