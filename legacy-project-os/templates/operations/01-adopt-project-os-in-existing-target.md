# Adoptar Project OS en Target Existente

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.target_adoption, mode.delegated_commit_pr.
  Browser chat drafts; a terminal agent performs any commit/PR under mode.delegated_commit_pr only with exact PM approval.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if target identity, adoption evidence, or PM approval for writes is missing or ambiguous.

LIVE_STATE:
  Inspect TARGET_REPOSITORY adoption state live: AGENTS.md, CLAUDE.md, GEMINI.md, any browser-chat adapter,
  metadata, roadmap anchor, kernel repo/path/version, target notes, and durable live-state risk.
  Read PM-provided context: code state, PM decisions, roadmap, fixed docs, open and recently closed issues.

DO:
  Detect which adoption files are missing or drifted against KERNEL_REPOSITORY adapters/*.target.md.
  Draft an adoption packet: adapter content from canonical templates filled for the target, plus an adoption checklist.
  Draft a delegated route-prompt (templates/route-prompt.md) that creates only AGENTS.md, CLAUDE.md, and GEMINI.md.

IF an adoption write is requested:
  Require exact scoped PM approval before any terminal-agent commit/PR; otherwise draft only.

OUTPUT:
  output.adoption_packet (plus a route-prompt when delegated creation is approved).

LIMITS:
  Adapter-only diff; no product code, CI/deploy/runtime config, secrets, settings, merge, close, label, tag, or release.
  Preserve target-owned notes, security/domain constraints, and validation commands.


RECOMMENDED_NEXT_OPERATION:
  Operation 03 (Verify target adoption).
