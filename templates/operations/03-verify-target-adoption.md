# Verificar Adopción en Repositorio Target

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.target_adoption, mode.review_only.
  A terminal agent may run this read-only against a local target checkout.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_QUESTION=<PM_QUESTION>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional


KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if target identity or adoption evidence cannot be read.

LIVE_STATE:
  Read target adapters (AGENTS.md, CLAUDE.md, GEMINI.md, any browser-chat adapter) and their metadata live.
  Compare kernel repo/path/version, roadmap anchor, and durable live-state risk against KERNEL_REPOSITORY adapters/*.target.md.

DO:
  Report whether adoption is present, correct, and references the current kernel.
  Name drift, stale baseline, roadmap mismatch, durable live-state content, and missing files.

OUTPUT:
  output.status_result with adoption findings; no fixes applied.

LIMITS:
  Read-only audit; no mutation of the target. Fixing drift is the upgrade operation, not this one.


RECOMMENDED_NEXT_OPERATION:
  Operation 05 (Review project state), 06 (Draft next issue), or 14 (Audit adapters).
