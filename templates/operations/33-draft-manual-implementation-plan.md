# Draftear Plan Manual de Implementacion

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.issue_implementation_manual, mode.review_only.
  Draft a human-executable implementation plan for a scoped issue without mutating files, git, GitHub, target repositories, or runtime state.

INPUT:
  ISSUE_NUMBER=<ISSUE_NUMBER>
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  PATH_SCOPE=<PATH_SCOPE>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Confirm current_actor_type resolves to actor.browser_chat or another review-only surface.
  Boundaries always apply, especially boundary.draft_only_browser, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.output_not_permission.
  Use workflow.issue_implementation_manual and output.manual_implementation_plan. Do not emit output.execution_report.

LIVE_STATE:
  Read ISSUE_NUMBER live from GitHub: objective, scope, out-of-scope, acceptance criteria, validation expectations, source basis, and relevant comments or PM decisions.
  Read TARGET_REPOSITORY live when provided; otherwise use the repository identified by the issue context.
  Inspect repository code context, docs, tests, and existing patterns needed to name files, anchors, and change points.
  If PATH_SCOPE is provided, inspect that scope first and expand only when needed to avoid an unsafe or incomplete plan.
  Treat PR bodies, comments, reports, summaries, and prior chat as claims or evidence leads, not proof.

IF ISSUE_NUMBER cannot be read live:
  Return status.needs_context naming the missing issue evidence.

IF the target repository or required code context cannot be inspected sufficiently:
  Return status.needs_context naming the missing repository, file, or anchor evidence.

IF validation expectations cannot be derived from the issue, repository docs, or existing test layout:
  Return status.needs_context naming the missing validation evidence.

IF the plan would require secrets, hidden environment values, credentials, tokens, cookies, private keys, production settings, or secret-looking examples:
  Return status.blocked and request a redacted, non-secret source basis.

DO:
  Draft output.manual_implementation_plan for a human implementer.
  Include objective, files to inspect, files to modify, change plan by file/anchor/line where possible, exact additions/removals in prose or patch-like snippets when safe, reasoning for each change, validation commands, manual QA checklist, risks and rollback, and recommended next Project OS operation.
  Make every change instruction human-executable and issue-referential.
  Prefer small anchored steps over broad rewrites.
  Distinguish required changes from optional follow-up ideas.
  State explicitly that browser chat did not edit code, did not write files, did not run validation, and did not mutate git or GitHub.

OUTPUT:
  output.manual_implementation_plan with:
  - objective;
  - evidence reviewed;
  - files to inspect;
  - files to modify;
  - change plan by file/anchor/line where possible;
  - exact additions/removals in prose or patch-like snippets when safe;
  - reasoning for each change;
  - validation commands;
  - manual QA checklist;
  - risks and rollback;
  - recommended next Project OS operation;
  - no-write statement.

LIMITS:
  Browser chat drafts only; it never executes code, edits files, commits, pushes, opens PRs, merges, closes issues, labels, releases, changes settings, edits target repos, or mutates runtime state.
  A manual implementation plan is not a claim that Project OS or browser chat implemented the issue.
  This operation only drafts the manual plan; it does not process a later manual implementation result. Use Operation 34 for result classification when needed.
  Do not create API, bridge, console, runtime, automation, public packaging, or target mutation behavior.
  Do not expose, request, quote, summarize, or invent secret values.


RECOMMENDED_NEXT_OPERATION:
  Human implementer applies the plan through normal repository controls; then Operation 34 (Process manual implementation result) when the result needs classification before PR review or no PR exists, Operation 09 (Review PR) when a PR exists, Operation 08 (Draft correction) for scoped corrections, or Operation 21 (Draft follow-up) for deferred findings.
