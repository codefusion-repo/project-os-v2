# MOS-R.5 audit-target-adoption-batch

MOSDLC:
  ID: MOS-R.5
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat / actor.terminal_agent
  Compatibility source: templates/operations/14-audit-target-adapters.md, templates/operations/03-verify-target-adoption.md
  Classification: accepted-recommended; variant (lote de MOS-0.5)
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state, evidence.target_adoption

OPERATION:
  Audit the adoption of multiple target projects in one batch, read-only, and consolidate drift per target.
  Source map summary: Audita en lote la adopción de múltiples proyectos target. Mantener varios proyectos adoptados sin drift. Itera la verificación de adopción por target y consolida drift.

INPUT:
  TARGET_REPOSITORIES=<TARGET_REPOSITORIES>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/14-audit-target-adapters.md and templates/operations/03-verify-target-adoption.md as compatibility sources for this recommended operation shape.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read each target repository's adapters, kernel adoption pointers, and adoption evidence live at execution time.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Read-only iteration of the single-target adoption verification over every repository in TARGET_REPOSITORIES, consolidating per-target drift, missing adapters, and stale kernel adoption.
  Return status.needs_context when TARGET_REPOSITORIES is empty or a listed target cannot be read; report unreadable targets explicitly instead of skipping them silently.
  Do not edit adapters, open PRs, or execute adoption updates for any target.

OUTPUT:
  output.status_result with the per-target adoption verdicts, consolidated drift, and the targets that need an adoption update.

LIMITS:
  Read-only batch audit; adoption updates per target are separate delegated operations with their own gates.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-0.4 per target with drift.
