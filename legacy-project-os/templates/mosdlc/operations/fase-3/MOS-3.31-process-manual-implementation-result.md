# MOS-3.31 process-manual-implementation-result

MOSDLC:
  ID: MOS-3.31
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/34-process-manual-implementation-result.md
  Classification: replacement
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.pm_command_bundle, output.route_prompt, output.status_result
  Evidence: evidence.issue_scope, evidence.repo_state, evidence.source_basis

OPERATION:
  Classify the result of human-applied manual implementation without claiming browser-chat execution.
  Source map summary: Procesa el resultado de la implementación manual aplicada por el humano. Clasificar la ruta segura tras aplicar un plan manual. Deriva a review de PR cuando existe PR; nunca duplica ese review.

INPUT:
  ISSUE_NUMBER=<ISSUE_NUMBER>
  MANUAL_IMPLEMENTATION_RESULT=<MANUAL_IMPLEMENTATION_RESULT>
  MANUAL_IMPLEMENTATION_PLAN=<MANUAL_IMPLEMENTATION_PLAN>   # optional
  PR_NUMBER=<PR_NUMBER>   # optional
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.review_before_close, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/34-process-manual-implementation-result.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 34 compatibility template.

LIVE_STATE:
  Read MANUAL_IMPLEMENTATION_RESULT, the manual plan when provided, issue scope, PR if any, repository evidence, and PM decisions live.
  Classify the human-applied result; browser chat did not edit code, validate code, or replace PR review.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Classify MANUAL_IMPLEMENTATION_RESULT into PR review, correction route, follow-up issue, PM decision, readiness review, or no-op.
  Route to MOS-3.7 when a PR exists and do not duplicate review-before-close.
  State that browser chat did not edit code, did not validate implementation, and only classified PM-provided evidence.
  Preserve manual implementation behavior as browser-chat and Human PM draft-only; never imply browser chat edited code.

OUTPUT:
  output.status_result plus output.route_prompt or output.pm_command_bundle only when classification selects that draft path.

LIMITS:
  Manual result classification only; browser chat never claims it edited code, validated code, or replaces review-before-close.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.7.
