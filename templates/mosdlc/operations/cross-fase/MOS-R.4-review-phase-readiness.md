# MOS-R.4 review-phase-readiness

MOSDLC:
  ID: MOS-R.4
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat
  Compatibility source: templates/operations/37-review-phase-readiness.md
  Classification: accepted-recommended; replacement
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state

OPERATION:
  Review advisory readiness before moving between MOSDLC phases, without executing any transition.
  Source map summary: Revisa readiness advisory antes de cambiar de fase MOSDLC. Gate transversal entre fases sin ejecutar transiciones. Read-only; identifica evidencia o decisiones faltantes.

INPUT:
  CURRENT_PHASE=<CURRENT_PHASE>   # optional
  TARGET_PHASE=<TARGET_PHASE>   # optional
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional
  PR_NUMBER=<PR_NUMBER>   # optional
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  ROADMAP_ISSUE=<ROADMAP_ISSUE>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/37-review-phase-readiness.md as compatibility source for this recommended operation shape.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read live phase evidence (issues, PRs, roadmap, docs, validation summaries) from GitHub and git at execution time.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Read-only advisory review of readiness to move from CURRENT_PHASE toward TARGET_PHASE, listing missing evidence, pending PM decisions, and blockers.
  Return status.needs_context when the phase evidence cannot be read, and status.needs_pm_decision when a phase transition needs an explicit PM choice.
  Do not approve, execute, or draft the phase transition itself.

OUTPUT:
  output.status_result with the readiness assessment, missing evidence or decisions, and the safe operation of the target phase.

LIMITS:
  Read-only and advisory; recommends but never executes, authorizes, or drafts the next phase's operations.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  The safe operation of the target phase when ready; MOS-R.3 when a PM decision is missing; MOS-R.2 when routing is unclear.
