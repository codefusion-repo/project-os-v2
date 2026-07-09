# MOS-4.8 draft-correction-from-qa

MOSDLC:
  ID: MOS-4.8
  Phase: Fase 4 - Testing / QA
  Surface: actor.browser_chat to actor.terminal_agent
  Compatibility source: templates/operations/08-draft-review-correction-route-prompt.md
  Classification: variant (fuente QA)
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.route_prompt
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Draft a non-authorizing correction route prompt from blocking QA results without expanding scope.
  Source map summary: Draftea el prompt de corrección desde resultados de QA. Corregir bloqueantes de QA sin expandir el scope. Encapsula el QA_RESULT en una ruta de corrección delegada.

INPUT:
  QA_RESULT=<QA_RESULT>
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional
  PR_NUMBER=<PR_NUMBER>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/08-draft-review-correction-route-prompt.md as compatibility source for this Fase 4 operation shape.
  Do not delete, rename, renumber, or bypass the 08 compatibility template.

LIVE_STATE:
  Read QA_RESULT, related issue or PR, acceptance evidence, validation expectations, and PM correction request live.
  Keep correction scope tied to blocking QA failures and the original issue or explicit PM-approved correction scope.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Summarize blocking QA findings and map each one to original issue, PR, or acceptance evidence.
  Draft output.route_prompt for the narrow correction scope, expected validation, and PM_AUTHORIZATION_STATUS.
  State that route prompts are non-authorizing outputs and that terminal writes require exact PM approval, branch preflight, validation, and draft PR review.
  Return status.needs_context when QA_RESULT, target issue or PR, feedback, or expected validation cannot be inspected.
  Do not execute corrections, edit files, create commits, push branches, comment on GitHub, close issues, merge PRs, or authorize implementation.

OUTPUT:
  output.route_prompt for a narrow QA correction, or output.status_result when issue, PR, QA feedback, or validation context is missing.

LIMITS:
  Correction route drafting only; route prompts are non-authorizing outputs and terminal writes require exact PM approval, branch preflight, validation, and draft PR review.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.7.
