# MOS-1.11 update-requirements-docs-existing

MOSDLC:
  ID: MOS-1.11
  Phase: Fase 1 - Requirements, planning, and feasibility
  Surface: actor.browser_chat to actor.terminal_agent
  Compatibility source: templates/operations/26-draft-docs-from-conversation.md, templates/operations/28-draft-docs-from-description.md
  Classification: variant; merge-candidate (con MOS-1.4 vía TARGET_REPOSITORY)
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.route_prompt, output.draft_issue, output.status_result
  Evidence: evidence.source_basis

OPERATION:
  Draft or update requirements documentation for an existing project from extracted requirements.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  DOC_TARGET=<DOC_TARGET>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Browser chat drafts with workflow.pm_intake and mode.review_only; terminal writes require a separate route prompt and exact PM approval.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/26-draft-docs-from-conversation.md and templates/operations/28-draft-docs-from-description.md as compatibility references for docs drafting.
  Do not delete, rename, renumber, or bypass the 26 or 28 compatibility templates.

LIVE_STATE:
  Read extracted requirements, target repository evidence, existing docs, issues, ADRs, and PM decisions live.
  Treat generated docs as draft content until exact PM approval routes terminal file writing.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft requirements docs for the existing project, separating observed evidence, inferred requirements, PM assumptions, and open questions.
  Identify DOC_TARGET only when PM input or live evidence makes the target path clear.
  If the PM asks to write a docs file, draft output.route_prompt with exact repository, path, scope, validation expectations, and PM authorization status.

OUTPUT:
  output.route_prompt only for separately approved terminal file creation; output.draft_issue when issue scope is safer; output.status_result when source basis or PM decisions are missing.

LIMITS:
  Browser chat drafts only and never writes files; terminal writes require exact PM approval, branch preflight, validation, and draft PR review.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-1.12 update-roadmap-existing.
