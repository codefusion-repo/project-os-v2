# MOS-3.5 draft-correction-route-prompt

MOSDLC:
  ID: MOS-3.5
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat to actor.terminal_agent
  Compatibility source: templates/operations/08-draft-review-correction-route-prompt.md
  Classification: replacement
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.route_prompt
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Draft a non-authorizing correction route prompt from actionable PR or issue feedback without expanding scope.
  Source map summary: Draftea el route-prompt de corrección de un PR/issue desde feedback accionable. Corregir sin expandir el scope original. Encapsula findings en una ruta de corrección delegada.

INPUT:
  ISSUE_NUMBER=<ISSUE_NUMBER>
  PR_NUMBER=<PR_NUMBER>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/08-draft-review-correction-route-prompt.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 08 compatibility template.

LIVE_STATE:
  Read the issue, PR, review feedback, validation evidence, and PM correction request live.
  Keep correction scope tied to the original issue or explicit PM-approved correction scope.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Summarize actionable findings and map each one to the original issue or PR evidence.
  Draft output.route_prompt for the narrow correction scope, expected validation, and PM_AUTHORIZATION_STATUS.
  Return status.needs_context when feedback, issue, PR, or expected validation cannot be inspected.
  Preserve route prompts as non-authorizing outputs; PM_AUTHORIZATION_STATUS is context, not permission.

OUTPUT:
  output.route_prompt for a narrow correction, or output.status_result when issue, PR, feedback, or validation context is missing.

LIMITS:
  Correction route drafting only; route prompts are non-authorizing outputs and terminal writes require exact PM approval, branch preflight, validation, and draft PR review.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.7.
