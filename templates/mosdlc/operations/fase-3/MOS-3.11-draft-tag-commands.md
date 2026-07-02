# MOS-3.11 draft-tag-commands

MOSDLC:
  ID: MOS-3.11
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/13-draft-create-release-tag-command.md
  Classification: replacement
  Workflow: workflow.release_readiness
  Mode: mode.review_only
  Output: output.pm_command_bundle
  Evidence: evidence.repo_state, evidence.validation_output

OPERATION:
  Draft a copy-safe git tag command bundle for the Human PM to execute after readiness is established.
  Source map summary: Draftea el bundle de creación de tag git para GitHub. Publicar un tag simple cuando el readiness lo justifica. Bundle copy-safe; el Humano PM ejecuta tag y push.

INPUT:
  TAG_NAME=<TAG_NAME>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.release_readiness with mode.review_only and emit only the declared output contracts.
  Apply boundary.copy_safe_commands, boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/13-draft-create-release-tag-command.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 13 compatibility template.

LIVE_STATE:
  Read release readiness, existing tags, target version, validation evidence, and PM tag decision live.
  Treat tag commands as a copy-safe PM bundle only; the template does not create tags.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft a copy-safe git tag and push bundle with exact tag name, repository, verification, risk, and rollback prose.
  Check for tag-name ambiguity or collisions from live evidence and stop for PM decision when needed.
  Do not create, push, delete, or move tags.
  Preserve release/tag behavior as PM-executed copy-safe command bundles only.

OUTPUT:
  output.pm_command_bundle with PM-executed tag commands and verification expectations.

LIMITS:
  Tag command drafting only; the Human PM executes any tag or push after separate exact approval.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.12.
