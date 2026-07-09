# MOS-4.7 draft-follow-up-from-qa

MOSDLC:
  ID: MOS-4.7
  Phase: Fase 4 - Testing / QA
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/21-draft-create-follow-up-from-review-command.md
  Classification: variant (fuente QA, no review de PR)
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.pm_command_bundle
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Draft a Human PM-executed follow-up issue bundle from non-blocking QA findings.
  Source map summary: Draftea follow-up desde resultados de QA. Diferir hallazgos de QA no bloqueantes con trazabilidad. Bundle de creación de follow-up para el Humano PM.

INPUT:
  QA_RESULT=<QA_RESULT>
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional
  PR_NUMBER=<PR_NUMBER>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.copy_safe_commands, boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/21-draft-create-follow-up-from-review-command.md as compatibility source for this Fase 4 operation shape.
  Do not delete, rename, renumber, or bypass the 21 compatibility template.

LIVE_STATE:
  Read QA_RESULT, related issue or PR when provided, acceptance evidence, and PM deferral decision live.
  Draft only non-blocking or explicitly deferred QA findings as follow-up work for the Human PM.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Extract non-blocking QA findings from QA_RESULT into one focused follow-up issue draft or a small bounded bundle when evidence requires separation.
  Draft output.pm_command_bundle for the Human PM with exact target repository placeholders and issue body.
  Do not include blocking QA failures that must return to MOS-4.8 before review-before-close.
  Do not execute the bundle, create issues, label issues, comment on GitHub, or authorize implementation.

OUTPUT:
  output.pm_command_bundle with a Human PM-executed QA follow-up issue creation bundle.

LIMITS:
  Draft-only operation; follow-up command bundles are PM-executed only and never authorize repository, GitHub, settings, release, tag, label, merge, closure, runtime-config, secret-store, product-code, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.4.
