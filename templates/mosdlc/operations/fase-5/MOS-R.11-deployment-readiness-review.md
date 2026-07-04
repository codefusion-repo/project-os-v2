# MOS-R.11 deployment-readiness-review

MOSDLC:
  ID: MOS-R.11
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat / actor.terminal_agent
  Compatibility source: none
  Classification: accepted-recommended; merge-candidate (unifica MOS-5.1, MOS-5.4 y MOS-5.7)
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis

OPERATION:
  Review deployment readiness for one environment selected by TARGET_ENVIRONMENT, read-only and parameterized.
  Source map summary: Revisa readiness de despliegue para un entorno dado vía TARGET_ENVIRONMENT. Unificar el análisis de readiness local/staging/producción. Una sola forma parametrizada que no colapsa las operaciones PM-facing por entorno.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  TARGET_ENVIRONMENT=<TARGET_ENVIRONMENT>
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
  This operation depends on the target actually having the TARGET_ENVIRONMENT deployment surface; not every target project has deployment environments. Read the target-owned Project-specific notes and repository deploy documentation live, and fail closed to status.needs_context when the environment does not apply to this target.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Read-only readiness review for TARGET_ENVIRONMENT: configuration presence, target-owned deploy commands, pending checklist items, and unresolved blockers, without collapsing the per-environment PM-facing operations.
  Report configuration and environment findings by file path, variable name, and risk type only; redact any sensitive or secret-looking value as [REDACTED] and never request secrets, print environment values, or run broad environment/config dumps.
  Return status.needs_context when deploy evidence is missing, conflicting, or the target has no such environment, and status.needs_pm_decision when readiness requires an explicit PM choice.
  Do not deploy, execute commands, edit configuration, or authorize deployment for any environment.

OUTPUT:
  output.status_result with the environment-scoped readiness assessment, gaps, and blockers, redacted by design.

LIMITS:
  Read-only readiness analysis; deployment execution and command drafting are separate operations with their own gates.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-R.12 when readiness is sufficient; otherwise the checklist operation of the corresponding environment.
