# MOS-3.12 draft-release-commands

MOSDLC:
  ID: MOS-3.12
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/24-draft-create-github-release-command.md
  Classification: replacement
  Workflow: workflow.release_readiness
  Mode: mode.review_only
  Output: output.pm_command_bundle
  Evidence: evidence.repo_state, evidence.validation_output

OPERATION:
  Draft a copy-safe GitHub Release command bundle for the Human PM to execute after readiness is established.
  Source map summary: Draftea el bundle de creación del objeto Release de GitHub (notas y tag). Publicar releases con notas trazables. Bundle copy-safe distinto del tag simple; ejecuta el Humano PM.

INPUT:
  TAG_NAME=<TAG_NAME>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.release_readiness with mode.review_only and emit only the declared output contracts.
  Apply boundary.copy_safe_commands, boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/24-draft-create-github-release-command.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 24 compatibility template.

LIVE_STATE:
  Read release readiness, existing tags/releases, release notes source, validation evidence, and PM release decision live.
  Treat release commands as a copy-safe PM bundle only; the template does not create releases.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft a copy-safe GitHub Release bundle with exact tag, title, notes source, repository, verification, risk, and rollback prose.
  Check for existing release/tag ambiguity from live evidence and stop for PM decision when needed.
  Do not create, edit, publish, delete, or mark releases latest.
  Preserve release/tag behavior as PM-executed copy-safe command bundles only.

OUTPUT:
  output.pm_command_bundle with PM-executed GitHub Release commands and verification expectations.

LIMITS:
  Release command drafting only; the Human PM executes any release creation after separate exact approval.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.1.
