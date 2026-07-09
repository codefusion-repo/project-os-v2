# MOS-3.28 draft-follow-up-from-audit

MOSDLC:
  ID: MOS-3.28
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/21-draft-create-follow-up-from-review-command.md
  Classification: variant (fuente auditoría, no review de PR)
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.pm_command_bundle
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Draft a follow-up issue from non-blocking implementation-discipline audit findings.
  Source map summary: Draftea follow-up desde la auditoría de gaps de disciplina. Diferir hallazgos no bloqueantes con trazabilidad. Bundle de creación de follow-up para el Humano PM.

INPUT:
  AUDIT_RESULT=<AUDIT_RESULT>
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional
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
  Read AUDIT_RESULT, related issue or PR, repository anchors, and PM deferral decision live.
  Draft only non-blocking or deferred findings as follow-up work for the Human PM.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Extract deferred implementation-discipline findings from AUDIT_RESULT into one focused follow-up issue draft.
  Draft output.pm_command_bundle for the Human PM with exact target repository and issue body.
  Do not include blocking corrections that must return to MOS-3.5 before closeout.

OUTPUT:
  output.pm_command_bundle with a Human PM-executed follow-up issue creation bundle.

LIMITS:
  Draft-only or read-only operation; no file, git, GitHub, settings, release, tag, label, merge, closure, runtime-config, secret-store, product-code, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.4.
