# Draftear Docs desde Descripción

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  Browser chat drafts documentation content from a PM description; terminal file creation requires exact PM approval.

INPUT:
  DESCRIPTION=<DESCRIPTION>
  DOC_TARGET=<DOC_TARGET> optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Required evidence: evidence.source_basis.
  Fail closed if DESCRIPTION lacks enough source basis for stable documentation.

LIVE_STATE:
  Read DESCRIPTION and any cited repository docs, issues, PRs, ADRs, or PM decisions live.

DO:
  Draft concise documentation content that separates stable rules/decisions from open questions.
  Identify the intended owning repository and file path only when the PM provided them or live evidence makes them clear.
  IF the PM asks to write a docs file, draft output.route_prompt per templates/route-prompt.md for terminal creation
  with exact repository, branch, scope, validation, and PM authorization status.
  IF the description is really implementation work, draft output.draft_issue instead of docs.

IF DOC_TARGET is needed but missing:
  Return status.needs_pm_decision naming the missing target repo/path or doc type.

OUTPUT:
  Draft documentation content for PM review, with output.route_prompt only for explicitly approved file creation.
  output.draft_issue when the safer next artifact is an issue.
  output.status_result when source basis, doc target, or PM decisions are missing.

LIMITS:
  Browser chat drafts only and never writes files. Do not include live issue/PR/branch/status state or secrets in durable docs.
