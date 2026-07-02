# MOS-0.6 handoff-session-context

MOSDLC:
  ID: MOS-0.6
  Phase: Fase 0 - Adaptation
  Surface: actor.browser_chat
  Compatibility source: templates/operations/17-draft-handoff-package-for-new-session.md
  Classification: replacement
  Workflow: workflow.handoff
  Mode: mode.review_only
  Output: output.handoff_packet
  Evidence: evidence.repo_state

OPERATION:
  Draft a handoff packet that lets a new session reconstruct context from live evidence.

INPUT:
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.handoff with mode.review_only.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/17-draft-handoff-package-for-new-session.md as the replacement source until MOSDLC migration is complete.
  Do not delete, rename, renumber, or bypass the 17 compatibility template.

LIVE_STATE:
  Read current source basis live enough to point the next session to authoritative evidence.
  Treat PM decisions not present in durable GitHub/git evidence as conversation context to summarize for immediate handoff only.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft a compact handoff packet with what was verified, what remains assumed, open PM decisions, active boundaries, and next operation.
  Point to categories of live evidence the next session must re-read rather than copying live state into durable docs.
  If live state cannot be reconstructed enough for handoff, return status.needs_context.

OUTPUT:
  output.handoff_packet for the PM to paste into the next session, or output.status_result when handoff cannot be drafted safely.

LIMITS:
  Never commit or save the handoff packet as durable repository state.
  No file, git, GitHub, settings, release, label, merge, closure, product-code, runtime-config, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-0.1 activate-browser-session in the new session.
