# Draftear Paquete de Handoff para Nueva Sesión

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.handoff, mode.review_only.

INPUT:
  PM_QUESTION=<PM_QUESTION>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional


KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the live state the packet must point to cannot be read.

LIVE_STATE:
  Read live: current conversation context, recent Human PM decisions, and current code state.
  Identify what is not yet captured in a durable PR/issue.

DO:
  Always prioritize Human PM decisions and recover the relevant conversation information for the handoff.
  Produce a compact handoff packet pointing to live GitHub evidence (issues, PRs, branches).

OUTPUT:
  output.handoff_packet the PM can paste into a new session.

LIMITS:
  Never store the packet as a durable file; memory lives in GitHub. No file, git, or GitHub mutation.


RECOMMENDED_NEXT_OPERATION:
  Start a new session with Operation 00 (Browser chat activation) using the packet.
