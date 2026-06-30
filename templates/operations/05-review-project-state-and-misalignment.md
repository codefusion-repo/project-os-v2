# Revisar Estado del Proyecto y Desalineaciones

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.review_only, mode.review_only.

INPUT:
  PM_QUESTION=<PM_QUESTION>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional


KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the live state required to judge alignment cannot be read.

LIVE_STATE:
  Read live: PM decisions and fixed docs (primary truth), roadmap, open issues, the most recent closed
  issues, and current code state. Treat comments and reports as claims or evidence leads.

DO:
  Take PM decisions and fixed docs as the main source of truth.
  Find misalignments in the roadmap, open issues, and recently closed issues.
  Find misalignments against the current code state.

IF PM_QUESTION present:
  Draft the answer using the live-state result as context.

OUTPUT:
  output.status_result carrying the misalignment findings by evidence reference and the safe next step
  (and the PM_QUESTION answer when asked).

LIMITS:
  Report only; do not create issues or assume resolutions. No file, git, or GitHub mutation.


RECOMMENDED_NEXT_OPERATION:
  Operation 06 (Draft next issue), 29 (Bounded roadmap), or 21 (Draft follow-up).
