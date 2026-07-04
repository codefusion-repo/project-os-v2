# MOS-R.7 review-licensing-publication-readiness

MOSDLC:
  ID: MOS-R.7
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat
  Compatibility source: templates/operations/12-analyze-release-or-tag-readiness.md
  Classification: accepted-recommended; new
  Workflow: workflow.release_readiness
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Review licensing, support posture, secrets hygiene, and documentation quality for publication readiness of the target project.
  Source map summary: Revisa licenciamiento, soporte, secrets hygiene y calidad de docs para publicación. Decidir publicación con revisión completa de release/publication readiness. Revisión read-only contra criterios de publicación del roadmap.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.release_readiness with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/12-analyze-release-or-tag-readiness.md as compatibility source for this recommended operation shape.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read the target repository's license files, support/maintenance statements, documentation, and publication criteria live; read the roadmap's publication criteria when they exist.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Read-only review of publication readiness: licensing completeness and compatibility, support posture, secrets hygiene, and documentation quality against the target's publication criteria.
  Report secret-hygiene findings by file path, variable name, and risk type only; never quote values.
  Return status.needs_context when publication criteria or repository evidence cannot be read, and status.needs_pm_decision when publication requires an explicit PM choice.
  Do not publish, tag, release, edit files, or authorize publication.

OUTPUT:
  output.status_result with the publication readiness assessment, gaps by area, and any PM decision required.

LIMITS:
  Read-only advisory review; publication decisions and actions remain with the Human PM.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-R.22.
