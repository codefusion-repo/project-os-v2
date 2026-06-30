# Recomendar Siguiente Operacion de Ciclo de Vida

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.review_only, mode.review_only.
  Recommend the next Project OS lifecycle operation from live traceability. Recommendation-only; never execute the next step.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional
  PR_NUMBER=<PR_NUMBER>   # optional
  ROADMAP_ISSUE=<ROADMAP_ISSUE>   # optional
  CURRENT_STATUS=<CURRENT_STATUS>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only, mode.review_only, and output.status_result.
  Boundaries always apply, especially boundary.draft_only_browser, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.output_not_permission.

LIVE_STATE:
  Read the provided ISSUE_NUMBER, PR_NUMBER, ROADMAP_ISSUE, TARGET_REPOSITORY, or CURRENT_STATUS live where applicable.
  If no anchor is provided, reconstruct only enough live GitHub/git state to identify the lifecycle position; do not invent hidden backlog or state.
  Treat PR bodies, comments, execution reports, manual results, validation summaries, and PM notes as claims or evidence leads until the target operation inspects its own required evidence.
  Compare evidence against docs/PM_OPERATIONS.md and docs/OPERATION_FLOWS.md to identify candidate operations.

IF no lifecycle anchor is provided and no single current context can be derived:
  Return status.needs_context naming the missing issue, PR, roadmap, repository, or status evidence.

IF multiple plausible lifecycle routes remain after reading evidence:
  Return status.needs_pm_decision with the candidate operations and the PM decision needed.

IF evidence contains secrets, hidden environment values, credentials, tokens, cookies, private keys, production settings, or secret-looking examples:
  Return status.blocked and request a redacted, non-secret source basis.

DO:
  Map the live evidence to the current SDLC phase.
  List candidate Project OS operations considered and why they do or do not fit.
  Recommend the safest next operation and name the evidence that the next operation must read.
  Prefer existing operations and existing kernel ids; do not add, imply, or execute lifecycle transitions.
  State explicitly that this is recommendation-only and does not run, authorize, or draft the recommended operation's output.
  If the next step would require write-capable terminal work, state that a separate exact PM-approved route prompt and branch preflight are required.

OUTPUT:
  output.status_result with:
  - current lifecycle position;
  - evidence reviewed;
  - candidate operations considered;
  - recommended next operation;
  - missing evidence or PM decision when applicable;
  - explicit recommendation-only statement.

LIMITS:
  Read-only and draft-only. No mutation.
  Do not execute the recommended operation.
  Do not replace Operation 36 when the task is processing status.needs_pm_decision.
  Do not replace Operation 37 when the task is phase readiness review.
  Do not emit output.route_prompt, output.pm_command_bundle, output.execution_report, or output.closure_comment.
  Do not create issues, branches, commits, PRs, comments, labels, tags, releases, settings changes, workflow automation, APIs, bridges, runtimes, public packages, or target-repo mutations.
  Do not implement #344/TOOLS.6 wizard lifecycle or output hygiene.
  Do not expose, request, quote, summarize, or invent secret values.

RECOMMENDED_NEXT_OPERATION:
  Human PM chooses whether to invoke the recommended operation. This operation stops after the recommendation.
