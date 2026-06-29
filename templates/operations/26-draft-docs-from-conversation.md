# Draftear Docs desde Conversación

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  Browser chat drafts documentation content; writing files is delegated to a terminal agent via route-prompt
  only under exact PM approval.

INPUT:
  CONVERSATION_CONTEXT=<CONVERSATION_CONTEXT>
  DOC_TARGET=<DOC_TARGET> optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Required evidence: evidence.source_basis.
  Fail closed if CONVERSATION_CONTEXT does not include enough source basis to separate stable decisions
  from live state, preference, or unresolved discussion.

LIVE_STATE:
  Read the PM-provided conversation context plus any cited issues, PRs, ADRs, docs, or decisions live.
  Treat conversation excerpts as source basis, not as authorization to write files.

DO:
  Extract stable decisions, constraints, rationale, and open questions from the conversation.
  Draft documentation content for PM review, or draft output.draft_issue if the conversation should become
  issue scope before docs are written.
  IF the PM explicitly approves a docs file write, draft output.route_prompt per templates/route-prompt.md
  for terminal file creation under workflow.issue_implementation or workflow.pm_intake as scoped by the PM.
  Keep live issue/PR/branch/status facts out of durable docs; point to live GitHub evidence instead.

IF stable doc content cannot be distinguished from unresolved discussion:
  Return status.needs_pm_decision with the specific decision needed.

OUTPUT:
  Draft documentation content for PM review, with output.route_prompt only when file creation is explicitly approved.
  output.draft_issue when the conversation should first become one scoped issue.
  output.status_result when source basis or PM decisions are missing.

LIMITS:
  Browser chat drafts only. This operation grants no file-write authority and stores no transcript as durable state.
  Redact secrets or secret-looking values as [REDACTED].
