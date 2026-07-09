# MOS-3.7 review-pr-before-close

MOSDLC:
  ID: MOS-3.7
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat
  Compatibility source: templates/operations/09-review-pr-before-close-and-draft-package.md
  Classification: replacement
  Workflow: workflow.review_before_close
  Mode: mode.review_only
  Output: output.pm_command_bundle, output.review_result
  Evidence: evidence.issue_scope, evidence.pr_diff, evidence.validation_output

OPERATION:
  Review a PR against the linked issue before any closeout package is drafted.
  Source map summary: Revisa el PR contra el issue vinculado antes de draftear cierre y limpieza. Gate de calidad previo a todo cierre. Compara diff, validación y scope; consume execution reports como evidence leads.

INPUT:
  PR_NUMBER=<PR_NUMBER>
  EXECUTION_REPORT=<EXECUTION_REPORT>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_before_close with mode.review_only and emit only the declared output contracts.
  Apply boundary.review_before_close, boundary.implementation_discipline, boundary.primary_path_discipline, boundary.validation_discipline, boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/09-review-pr-before-close-and-draft-package.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 09 compatibility template.

LIVE_STATE:
  Read the linked issue objective, scope, out-of-scope, acceptance criteria, PR changed files, diff, final files when needed, validation, and reports live.
  Treat execution reports and PR bodies as evidence leads, not proof of implementation.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Compare issue objective, scope, out-of-scope, and acceptance criteria against changed files, diff, final files when needed, validation evidence, and docs/VALIDATION_POLICY.md.
  Accept scoped PM-run command output, manual PM validation, or a justified no-automated-check exception only when mandatory validation was not required by risk.
  Fail closed when mandatory validation is missing for kernel, resolver, security, authorization, traceability, deployment, secret-sensitive, production-impacting, or deterministic contract changes.
  Report findings before summary and draft closeout only when code-backed review resolves the issue.
  Return status.needs_context instead of GO when code, diff, final-file, issue, PR, or validation evidence cannot be inspected.
  Preserve review-before-close behavior; this template does not merge or close.

OUTPUT:
  output.review_result with findings and verdict; output.pm_command_bundle only as a drafted closeout package when review resolves.

LIMITS:
  Review-only; the template does not merge, close, label, mark ready, delete branches, or treat execution reports as proof.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.6.
