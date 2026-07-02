# MOS-1.4 draft-requirements-docs

MOSDLC:
  ID: MOS-1.4
  Phase: Fase 1 - Requirements, planning, and feasibility
  Surface: actor.browser_chat to actor.terminal_agent
  Compatibility source: templates/operations/26-draft-docs-from-conversation.md, templates/operations/28-draft-docs-from-description.md
  Classification: replacement
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.route_prompt, output.draft_issue, output.status_result
  Evidence: evidence.source_basis

OPERATION:
  Draft functional and non-functional requirements, use cases, and user stories from stable Fase 1 source basis.

INPUT:
  DOC_TARGET=<DOC_TARGET>   # optional
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Browser chat drafts with workflow.pm_intake and mode.review_only; terminal writes require a separate route prompt and exact PM approval.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/26-draft-docs-from-conversation.md and templates/operations/28-draft-docs-from-description.md as replacement sources for docs drafting shape.
  Do not delete, rename, renumber, or bypass the 26 or 28 compatibility templates.

LIVE_STATE:
  Read requirement summaries, feasibility findings, cited docs, ADRs, issues, PRs, and PM decisions live.
  Treat generated docs as draft content until the PM approves an exact write route.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft requirements docs that separate functional requirements, non-functional requirements, use cases, user stories, constraints, assumptions, and open questions.
  If the PM asks to write a docs file, draft output.route_prompt with exact repository, path, scope, validation expectations, and PM authorization status.
  Return output.draft_issue instead of docs when the source basis is implementation scope rather than durable documentation.

OUTPUT:
  output.route_prompt only for separately approved terminal file creation; output.draft_issue when issue scope is safer; output.status_result when source basis or PM decisions are missing.

LIMITS:
  Browser chat drafts only and never writes files; terminal writes require exact PM approval, branch preflight, validation, and draft PR review.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-1.5 validate-requirements-docs.
