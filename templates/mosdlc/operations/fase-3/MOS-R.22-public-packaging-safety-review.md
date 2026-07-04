# MOS-R.22 public-packaging-safety-review

MOSDLC:
  ID: MOS-R.22
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat
  Compatibility source: none
  Classification: accepted-recommended; new
  Workflow: workflow.release_readiness
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Review the safety of packaging the target project for public use, read-only.
  Source map summary: Revisa la seguridad de empaquetar el target para uso público. Evitar publicar superficies internas o inseguras. Revisión read-only de secrets hygiene, docs y superficies internal-only del target.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.release_readiness with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  No 00-37 compatibility source is mapped for this recommended operation.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read the target repository's packaging surfaces, documentation, and internal-only inventory live; not every target project has public packaging, so fail closed to status.needs_context when no public packaging surface exists.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Read-only safety review before public packaging: secrets hygiene, internal-only surfaces that must be removed/hidden/disabled/converted before release, documentation exposure, and unsafe defaults.
  Report secret-hygiene findings by file path, variable name, and risk type only; redact values as [REDACTED].
  Return status.needs_context when packaging surfaces cannot be read, and status.needs_pm_decision when a surface's exposure requires an explicit PM choice.
  Do not package, publish, release, edit files, or convert internal-only surfaces.

OUTPUT:
  output.status_result with the packaging-safety findings, the internal-only surfaces pending pre-release conversion, and any PM decision required.

LIMITS:
  Read-only advisory review; conversions and publication are separate operations with their own gates.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-R.23.
