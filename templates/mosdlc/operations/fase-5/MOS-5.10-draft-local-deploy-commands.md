# MOS-5.10 draft-local-deploy-commands

MOSDLC:
  ID: MOS-5.10
  Phase: Fase 5 - Despliegue local / staging / produccion
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: none
  Classification: new; merge-candidate (via TARGET_ENVIRONMENT, ver MOS-R.12)
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.pm_command_bundle
  Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis

OPERATION:
  Draft a local deployment command bundle for Human PM execution only, using strictly target-owned local deploy commands.
  Source map summary: Draftea el bundle de comandos de despliegue local desde comandos target-owned de Project-specific notes. Preparar ejecucion local sin inventar comandos. Bundle copy-safe solo desde comandos target-owned; nunca imprime secretos.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.copy_safe_commands, boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  No 00-37 compatibility source is mapped for this Fase 5 operation.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read target-owned Project-specific notes, local deploy command notes, adoption notes, repository docs, and MOS-5.3 checklist classification live.
  Treat local deploy commands as a Human PM-executed output.pm_command_bundle only; the template does not execute them.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft only commands that already exist in target-owned notes or repository deploy documentation; preserve exact command names and targets from evidence.
  Fail closed to status.needs_context when local deploy commands are missing, conflicting, incomplete, environment-specific but unscoped, or ambiguous.
  Keep scope, risk, rollback, secret-safety, and verification prose outside executable blocks and follow templates/pm-command-bundle.md.
  If GitHub verification appears, use supported gh --json state,isDraft,mergeable,mergeStateStatus,headRefName,headRefOid,mergedAt,closedAt fields only.
  Redact sensitive values as [REDACTED] and reference only variable names or risk types.
  Do not execute the bundle, invent commands, request secrets, print environment values, run broad environment/config dumps, or authorize local deployment.

OUTPUT:
  output.pm_command_bundle for Human PM-executed local deploy commands, or a fail-closed status when evidence is insufficient.

LIMITS:
  Command drafting only; the Human PM decides and executes any local deploy command after separate exact approval.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-5.11 only with separate exact deploy approval and candidate handling; otherwise Human PM execution followed by MOS-R.13.
