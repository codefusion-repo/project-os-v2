# MOS-R.17 dependency-security-update-audit

MOSDLC:
  ID: MOS-R.17
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat
  Compatibility source: none
  Classification: accepted-recommended; new
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state

OPERATION:
  Audit dependencies and pending security updates for the target project, read-only, with severity and a proposed update route.
  Source map summary: Audita dependencias y actualizaciones de seguridad pendientes. Reducir riesgo de dependencias sin ejecutar upgrades a ciegas. Auditoría read-only con severidad y ruta de actualización propuesta.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
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
  Read the target repository's dependency manifests, lockfiles, and security advisories live at execution time.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Read-only audit of dependencies and pending security updates, classifying each finding by severity and proposing a prioritized update route without executing any upgrade.
  Redact any credentials or secret-looking values found in dependency configuration as [REDACTED]; report registry or configuration risks by file path, variable name, and risk type only, and never request secrets.
  Return status.needs_context when dependency manifests or advisory data cannot be read.
  Do not run upgrades, edit manifests, pin versions, or execute installs.

OUTPUT:
  output.status_result with the prioritized findings, severity per dependency, and the proposed update route.

LIMITS:
  Read-only audit; dependency upgrades are separate scoped issues with their own gates.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.8 for prioritized upgrades; MOS-3.3 for non-urgent follow-ups.
