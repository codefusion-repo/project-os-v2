# Procesar Decision PM Requerida

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  Process a Project OS status.needs_pm_decision result without auto-approving, auto-executing, or crossing the originating operation boundary.

INPUT:
  ORIGINATING_OPERATION=<ORIGINATING_OPERATION>
  STATUS_CONTEXT=<STATUS_CONTEXT>
  OPTIONS_TRADEOFFS=<OPTIONS_TRADEOFFS>
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional
  PR_NUMBER=<PR_NUMBER>   # optional
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  ROADMAP_ISSUE=<ROADMAP_ISSUE>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake, mode.review_only, output.status_result, output.route_prompt, output.pm_command_bundle, and output.draft_issue.
  Boundaries always apply, especially boundary.draft_only_browser, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.output_not_permission.

LIVE_STATE:
  Read ORIGINATING_OPERATION as the operation/template/status source that produced status.needs_pm_decision.
  Read STATUS_CONTEXT and OPTIONS_TRADEOFFS as claims or evidence leads, not proof.
  Read ISSUE_NUMBER, PR_NUMBER, TARGET_REPOSITORY, and ROADMAP_ISSUE live when provided.
  If the originating operation can be identified in templates/operations or docs/PM_OPERATIONS.md, compare the requested decision against that operation's workflow, output, limits, and recommended next operation.
  Treat PR bodies, issue comments, execution reports, validation summaries, PM notes, and prior route prompts as claims or evidence leads until the target operation inspects its required evidence.

IF ORIGINATING_OPERATION, STATUS_CONTEXT, or OPTIONS_TRADEOFFS is missing or too vague to identify the decision point:
  Return status.needs_context naming the missing origin, status context, or options/tradeoffs.

IF provided issue, PR, roadmap, or target repository evidence cannot be read live or conflicts with the originating operation:
  Return status.needs_context naming the missing or conflicting live evidence.

IF the choice changes product/process policy, accepts an exception, expands scope, or selects between materially different lifecycle routes and PM_FEEDBACK_HUMANO does not make the decision explicit:
  Return status.needs_pm_decision naming the exact PM decision still required.

IF evidence contains secrets, hidden environment values, credentials, tokens, cookies, private keys, production settings, or secret-looking examples:
  Return status.blocked and request a redacted, non-secret source basis.

DO:
  Classify the status.needs_pm_decision result into exactly one safe outcome:
  - PM decision recorded for the originating operation.
  - Missing context that must be supplied before any route can continue.
  - Correction route to Operation 08 when scoped implementation corrections are needed.
  - Follow-up issue draft through Operation 21 or output.draft_issue when non-blocking work should be tracked separately.
  - Stop/no-op when the PM chooses not to proceed.
  - Route prompt when a new terminal-agent action is needed and exact scoped approval can be drafted for PM review.
  Preserve PM authority: do not infer approval, do not execute the selected route, and do not treat a decision as write permission unless the future write operation independently receives exact PM approval and satisfies its own gates.
  Prefer returning the decision to the originating operation when that operation can safely continue.
  Use PM_FEEDBACK_HUMANO as PM interpretation or decision evidence only for the point explicitly decided.
  Use PM_QUESTION_HUMANO, if present, to narrow the decision question without replacing required evidence.

OUTPUT:
  output.status_result with:
  - originating operation/status context;
  - live evidence reviewed;
  - options/tradeoffs considered;
  - PM decision, missing context, correction route, follow-up issue, stop/no-op, or route prompt classification;
  - any remaining evidence or PM decision required;
  - explicit statement that no approval or lifecycle transition was executed.
  If scoped corrections are needed, draft output.route_prompt for Operation 08.
  If follow-up work should be tracked, draft output.pm_command_bundle for Operation 21 or output.draft_issue content for PM review.

LIMITS:
  Draft only. No mutation. No merge, close, labels, releases, settings changes, file edits, commits, pushes, PR creation, or automated lifecycle transition.
  Does not auto-approve PM decisions, terminal-agent writes, follow-up creation, route execution, merge, closeout, release, or cleanup.
  Does not replace the originating operation's evidence checks.
  Does not create a hidden workflow engine or execute lifecycle transitions automatically.
  Does not process terminal-agent execution reports for normal PR review; Operation 09 remains that path when a PR exists.
  Does not implement #344/TOOLS.6 wizard lifecycle or output hygiene.
  Does not expose, request, quote, summarize, or invent secret values.

RECOMMENDED_NEXT_OPERATION:
  Return to the originating operation if the PM decision is sufficient; Operation 08 for scoped corrections; Operation 21 for follow-up drafts; Operation 35 when only route recommendation is still needed; otherwise stop with status.needs_context or status.needs_pm_decision.
