# Analizar Idea como Feature del Sistema

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.review_only, mode.review_only.

INPUT:
  IDEA=<IDEA>

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the live state needed to judge fit cannot be read.

LIVE_STATE:
  Read live: current code state, PM decisions, roadmap, fixed docs (including docs/DESIGN.md),
  open issues, and the most recent closed issues.

DO:
  Determine whether IDEA is viable as a feature within the system (kernel, roadmap, code).
  IF viable, propose next steps to integrate it without breaking anything.
  Name risks, redundancies, and plausible code locations.

OUTPUT:
  output.status_result with the feasibility diagnosis and recommended next steps.

LIMITS:
  Report only; do not turn the idea into an issue without an explicit PM decision. No mutation.
