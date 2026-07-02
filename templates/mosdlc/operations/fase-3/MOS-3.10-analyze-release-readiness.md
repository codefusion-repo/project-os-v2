# MOS-3.10 analyze-release-readiness

MOSDLC:
  ID: MOS-3.10
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat
  Compatibility source: templates/operations/12-analyze-release-or-tag-readiness.md, templates/operations/13-draft-create-release-tag-command.md
  Classification: replacement; merge-candidate (análisis de 12 más drafteo de 13)
  Workflow: workflow.release_readiness
  Mode: mode.review_only
  Output: output.pm_command_bundle, output.status_result
  Evidence: evidence.repo_state, evidence.validation_output

OPERATION:
  Analyze tag or release readiness from merged evidence and validation, and draft command bundles only when ready.
  Source map summary: Analiza readiness de release-on-tag y draftea los comandos de creación si está listo. Decidir tag/release con evidencia merged y validación. Evalúa readiness y encadena el drafteo del bundle solo si procede.

INPUT:
  TAG_NAME=<TAG_NAME>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.release_readiness with mode.review_only and emit only the declared output contracts.
  Apply boundary.copy_safe_commands, boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/12-analyze-release-or-tag-readiness.md, templates/operations/13-draft-create-release-tag-command.md as compatibility sources for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 12, 13 compatibility templates.

LIVE_STATE:
  Read merged outcomes, validation evidence, release notes candidates, tags, open risks, and PM release intent live.
  Treat readiness as advisory; tag or release creation remains a separate Human PM action.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Assess whether merged scope, validation, known risks, notes, and version/tag intent support a tag or release.
  Draft output.pm_command_bundle only as a PM-executed candidate when readiness is sufficient and target is exact.
  Return status.needs_context or status.needs_pm_decision for missing validation, unresolved scope, tag naming, notes, or risk decisions.
  Preserve release/tag behavior as PM-executed copy-safe command bundles only.

OUTPUT:
  output.status_result with readiness findings; output.pm_command_bundle only as a drafted PM-executed candidate when ready.

LIMITS:
  Release readiness review only; no tag, release, branch, settings, deployment, or GitHub mutation authority.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.11.
