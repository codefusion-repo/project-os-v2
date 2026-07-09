# MOS-R.20 review-validation-cycle-readiness

MOSDLC:
  ID: MOS-R.20
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat
  Compatibility source: templates/operations/37-review-phase-readiness.md
  Classification: accepted-recommended; variant (readiness de ciclo de validación)
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state

OPERATION:
  Review readiness to start or close a validation cycle for the target project, read-only and advisory.
  Source map summary: Revisa readiness para iniciar o cerrar un ciclo de validación del target. Entrar y salir del ciclo de validación con criterios claros. Revisión advisory read-only de los criterios de validación del target.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  VALIDATION_CYCLE_TYPE=<VALIDATION_CYCLE_TYPE>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

  VALIDATION_CYCLE_TYPE names the validation surface that fits the target project type: internal QA, staging validation, beta rollout, or UAT for web apps; TestFlight/internal testing or release candidate validation for mobile apps; playtest, balance test, content QA, or performance validation for games; integration test, consumer validation, or release candidate trial for libraries and tools; pilot rollout, acceptance test, or operational validation for internal systems.

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/37-review-phase-readiness.md as compatibility source for this recommended operation shape.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  This operation depends on the target actually having an applicable validation surface; fail closed to status.needs_context when none applies.
  Read the cycle's entry/exit criteria, planned issues, and live evidence at execution time.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Read-only advisory review of the cycle's entry criteria (to start) or exit criteria (to close), listing missing evidence, unresolved blockers, and pending PM decisions.
  Return status.needs_context when the cycle criteria or evidence cannot be read, and status.needs_pm_decision when starting or closing the cycle requires an explicit PM choice.
  Do not start, close, extend, or execute any part of the validation cycle.

OUTPUT:
  output.status_result with the readiness assessment against the cycle's criteria and any missing evidence or decisions.

LIMITS:
  Read-only and advisory; the Human PM decides cycle start and close.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-R.21 when closing the cycle.
