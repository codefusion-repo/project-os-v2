# MOS-0.1 activate-browser-session

MOSDLC:
  ID: MOS-0.1
  Phase: Fase 0 - Adaptation
  Surface: actor.browser_chat
  Compatibility source: templates/operations/00-browser-chat-activation.md
  Classification: replacement
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state

OPERATION:
  Establish the PM browser-chat session context as draft-only and prepare safe MOSDLC routing.

INPUT:
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Confirm the current surface resolves to actor.browser_chat.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/00-browser-chat-activation.md as the replacement source until MOSDLC migration is complete.
  Do not delete, rename, renumber, or bypass the 00 compatibility template.

LIVE_STATE:
  Read repository state from GitHub/git only when the current PM request needs it.
  Treat comments, reports, summaries, and prior prompts as claims or evidence leads until verified live.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Confirm kernel resolution and browser-chat draft-only posture.
  Identify the safe next MOSDLC Fase 0 operation from the PM request and live evidence.
  If write-capable work is needed, route to a terminal agent through a separate route prompt and exact PM approval.

OUTPUT:
  output.status_result with actor, draft-only context, evidence read, missing context if any, and safe next operation.

LIMITS:
  Browser chat drafts only; no file, git, GitHub, settings, release, label, merge, closure, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-0.2, MOS-0.3, or MOS-0.5 depending on target adoption state; MOS-0.6 for handoff.
