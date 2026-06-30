# Auditar Brechas de Disciplina de Implementación

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.implementation_discipline_audit, mode.review_only.
  A terminal agent may run the same read-only audit against a local checkout.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PATH_SCOPE=<PATH_SCOPE>   # optional
  FOCUS=<FOCUS>   # optional
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional
  PR_NUMBER=<PR_NUMBER>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use boundary.implementation_discipline as the canonical audit rule.
  Fail closed if required code or live issue/PR evidence cannot be inspected.

LIVE_STATE:
  Read TARGET_REPOSITORY live from GitHub and/or the local checkout.
  If ISSUE_NUMBER is provided, read the issue objective, scope, out-of-scope, and acceptance criteria live.
  If PR_NUMBER is provided, read the PR changed files, diff, comments, and relevant final head files.
  If PATH_SCOPE or FOCUS is provided, restrict inspection to that requested area unless evidence shows the scope is insufficient.

DO:
  Inspect codebase structure and selected files for evidence-backed implementation-discipline gaps.
  Map every finding to boundary.implementation_discipline, not to a separate style guide.
  Classify each finding by severity or follow-up priority.
  Identify acceptable local tradeoffs and explicit project conventions as non-findings.
  Recommend or draft follow-up issues when useful.

IF code evidence cannot be inspected:
  Return status.needs_context. Name the missing source.

IF follow-up issue drafts are useful:
  Draft output.draft_issue content for PM review only. Do not create issues.

OUTPUT:
  output.review_result with scope reviewed, evidence reviewed, implementation-discipline findings, file/line references where possible, severity or priority, boundary mapping, acceptable tradeoffs, recommended follow-up issues, risks, and what was not reviewed.

LIMITS:
  Read-only audit; never refactor, edit files, commit, push, merge, close, label, or mutate GitHub from browser_chat.
  Do not duplicate a Clean Code manifesto; keep boundary.implementation_discipline as the source rule.
  Do not expose secrets, credentials, .env values, private keys, cookies, database URLs, CI secrets, or secret-looking values.


RECOMMENDED_NEXT_OPERATION:
  If gaps found, Operation 08 (Draft correction) or 21 (Draft follow-up).
