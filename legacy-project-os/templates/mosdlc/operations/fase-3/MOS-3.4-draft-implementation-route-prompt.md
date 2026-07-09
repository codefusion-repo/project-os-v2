# MOS-3.4 draft-implementation-route-prompt

MOSDLC:
  ID: MOS-3.4
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat to actor.terminal_agent
  Compatibility source: templates/operations/07-draft-issue-implementation-route-prompt.md
  Classification: replacement
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.route_prompt
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Draft a non-authorizing route prompt for delegated terminal-agent implementation of one scoped issue.
  Source map summary: Draftea el route-prompt para delegar la implementación de un issue a un terminal agent. Rutear implementación con scope, modo y evidencia correctos. Bootloader compacto; el detalle vive en el issue; nunca autoriza por sí mismo.

INPUT:
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional
  ROADMAP_ISSUE=<ROADMAP_ISSUE>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/07-draft-issue-implementation-route-prompt.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 07 compatibility template.

LIVE_STATE:
  Read the selected issue, roadmap anchor, source basis, target repository context, and PM authorization status live.
  Treat output.route_prompt as a routing packet only; it never grants terminal write permission by itself.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft output.route_prompt with exact repository, issue, branch naming expectation, workflow.issue_implementation, execution mode, proportional validation expectations, and PM_AUTHORIZATION_STATUS.
  Classify validation via docs/VALIDATION_POLICY.md as agent-run required commands, PM-run drafted commands, manual PM validation, or justified no automated validation.
  State that the executing terminal agent must re-resolve kernel/manifest.json, read the issue live, perform branch preflight, validate, and report.
  Keep PM command bundles or route prompts non-authorizing; permission comes only from exact scoped PM approval plus kernel gates.
  Preserve route prompts as non-authorizing outputs; PM_AUTHORIZATION_STATUS is context, not permission.

OUTPUT:
  output.route_prompt with exact scope and non-authorizing PM_AUTHORIZATION_STATUS language, or output.status_result when routing evidence is missing.

LIMITS:
  Route prompt drafting only; route prompts are non-authorizing outputs and terminal writes require exact PM approval, branch preflight, validation, and draft PR review.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.7.
