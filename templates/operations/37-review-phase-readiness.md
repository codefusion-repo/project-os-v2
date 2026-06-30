# Revisar Readiness de Fase

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.review_only, mode.review_only.
  Review advisory readiness before moving into implementation, manual implementation, QA/security/design, PR closeout, release, dogfood, or handoff.

INPUT:
  CURRENT_PHASE=<CURRENT_PHASE>   # optional
  TARGET_PHASE=<TARGET_PHASE>   # optional
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional
  PR_NUMBER=<PR_NUMBER>   # optional
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  ROADMAP_ISSUE=<ROADMAP_ISSUE>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only, mode.review_only, and output.status_result.
  Boundaries always apply, especially boundary.draft_only_browser, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.output_not_permission.

LIVE_STATE:
  Read CURRENT_PHASE or TARGET_PHASE as the requested readiness gate.
  Read ISSUE_NUMBER, PR_NUMBER, TARGET_REPOSITORY, and ROADMAP_ISSUE live when provided.
  Read branch/PR state, open blockers, linked issue scope, validation evidence, gate evidence, and PM decisions from GitHub/git where the surface can inspect them.
  Compare live evidence against docs/PM_OPERATIONS.md, docs/OPERATION_FLOWS.md, and the target operation template for the next phase.
  Treat PR bodies, issue comments, execution reports, validation summaries, PM notes, manual results, and route prompts as claims or evidence leads until the target operation inspects its required evidence.

IF neither CURRENT_PHASE nor TARGET_PHASE is provided and no single phase transition can be derived from live evidence:
  Return status.needs_context naming the missing current or target phase evidence.

IF the target phase is ambiguous or the PM must choose between materially different next phases:
  Return status.needs_pm_decision naming the candidate phases and the PM decision required.

IF required issue, PR, repository, roadmap, validation, gate, branch, or PM decision evidence cannot be inspected:
  Return status.needs_context naming the missing evidence and the operation that should provide it.

IF readiness depends on accepting a risk, skipping a gate, expanding scope, or changing product/process policy:
  Return status.needs_pm_decision naming the exact exception or decision required.

IF evidence contains secrets, hidden environment values, credentials, tokens, cookies, private keys, production settings, or secret-looking examples:
  Return status.blocked and request a redacted, non-secret source basis.

DO:
  Identify the current lifecycle position and requested target phase.
  Review readiness before moving into implementation, manual implementation, QA/security/design, PR closeout, release, dogfood, or handoff.
  Identify missing scope, validation, PM decisions, open blockers, branch or PR state, gate evidence, and any conflicting live evidence.
  Recommend the safest next Project OS operation and name the evidence that operation must read.
  Fail closed when evidence is insufficient; do not normalize missing evidence into a pass.
  State explicitly that this is advisory/read-only and does not run, authorize, or draft the recommended operation's output.
  If a write-capable next step is recommended, state that a separate exact PM-approved route prompt, branch preflight, and validation are required.

OUTPUT:
  output.status_result with:
  - current phase and target phase;
  - live evidence reviewed;
  - readiness verdict;
  - missing evidence, blockers, PM decisions, or accepted exceptions needed;
  - recommended next safe operation;
  - explicit advisory/read-only statement.

LIMITS:
  Read-only and advisory. No mutation.
  Do not execute lifecycle transitions automatically.
  Do not approve implementation, manual implementation, QA/security/design, PR closeout, release, dogfood, or handoff.
  Do not emit output.route_prompt, output.pm_command_bundle, output.execution_report, output.review_result, or output.closure_comment.
  Do not create issues, branches, commits, PRs, comments, labels, tags, releases, settings changes, workflow automation, APIs, bridges, runtimes, public packages, or target-repo mutations.
  Does not implement #344/TOOLS.6 wizard lifecycle or output hygiene.
  Do not expose, request, quote, summarize, or invent secret values.

RECOMMENDED_NEXT_OPERATION:
  Operation 36 when a PM decision blocks readiness; Operation 35 when the next operation itself is unclear; otherwise the safest operation for the target phase, invoked separately by the Human PM.
