# MOS-3.29 draft-follow-up-from-security

MOSDLC:
  ID: MOS-3.29
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/21-draft-create-follow-up-from-review-command.md
  Classification: variant (fuente seguridad, no review de PR)
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.pm_command_bundle
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Draft a follow-up issue from non-blocking security review findings.
  Source map summary: Draftea follow-up desde la revisión de seguridad. Diferir findings de seguridad no bloqueantes con trazabilidad. Bundle de creación de follow-up para el Humano PM.

INPUT:
  SECURITY_REVIEW_RESULT=<SECURITY_REVIEW_RESULT>
  PR_NUMBER=<PR_NUMBER>   # optional
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
  Read SECURITY_REVIEW_RESULT, related PR, issue, repository anchors, and PM deferral decision live.
  Draft only non-blocking or deferred security findings as follow-up work for the Human PM.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Extract deferred security findings from SECURITY_REVIEW_RESULT into one focused follow-up issue draft.
  Draft output.pm_command_bundle for the Human PM with exact target repository and issue body.
  Do not include secret values or blocking security corrections that must return to MOS-3.5 before closeout.
  Apply strict secret redaction; report only paths, variable names, risk types, and [REDACTED] placeholders when sensitive values appear.

OUTPUT:
  output.pm_command_bundle with a Human PM-executed follow-up issue creation bundle and redacted security context.

LIMITS:
  Draft-only or read-only operation; no file, git, GitHub, settings, release, tag, label, merge, closure, runtime-config, secret-store, product-code, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.4.
