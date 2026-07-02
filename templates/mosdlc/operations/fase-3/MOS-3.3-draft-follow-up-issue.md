# MOS-3.3 draft-follow-up-issue

MOSDLC:
  ID: MOS-3.3
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/21-draft-create-follow-up-from-review-command.md
  Classification: variant (fuente issue incompleto, no review)
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.pm_command_bundle
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Draft a follow-up issue for incomplete work without reopening or expanding the original issue scope.
  Source map summary: Draftea un issue de follow-up desde un issue incompleto. No perder trabajo pendiente cuando un issue cierra incompleto. Aísla lo faltante en un follow-up con scope propio.

INPUT:
  ISSUE_NUMBER=<ISSUE_NUMBER>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.copy_safe_commands, boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/21-draft-create-follow-up-from-review-command.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 21 compatibility template.

LIVE_STATE:
  Read the incomplete issue, related PRs, comments, validation evidence, and PM decisions live.
  Treat the follow-up as new scoped work, not as hidden expansion of the original issue.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Extract only the unfinished or explicitly deferred work from the incomplete issue evidence.
  Draft output.pm_command_bundle for a follow-up issue with its own objective, scope, out-of-scope, acceptance criteria, and validation.
  Do not use follow-up drafting to bypass review-before-close or hide blocking defects.

OUTPUT:
  output.pm_command_bundle with a focused follow-up issue creation bundle, or output.status_result when source evidence is insufficient.

LIMITS:
  Draft-only or read-only operation; no file, git, GitHub, settings, release, tag, label, merge, closure, runtime-config, secret-store, product-code, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.4.
