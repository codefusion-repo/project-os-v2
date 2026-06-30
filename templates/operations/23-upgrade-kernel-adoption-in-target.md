# Actualizar Adopción de Kernel en Target

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.target_adoption, mode.delegated_commit_pr.
  Browser chat drafts; a terminal agent applies the update under mode.delegated_commit_pr only with exact PM approval.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_QUESTION=<PM_QUESTION>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional


KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if target identity, adoption evidence, or PM approval for writes is missing or ambiguous.

LIVE_STATE:
  Read live: current target adapters, the declared adopted kernel version vs the current canonical version,
  and roadmap anchors.

DO:
  Detect version drift, stale baseline, and roadmap mismatch between target adapters and the canonical kernel.
  Draft an adoption packet with the adapter-update diff for AGENTS.md, CLAUDE.md, GEMINI.md and an update checklist.
  Draft a delegated route-prompt (templates/route-prompt.md) when the PM approves applying the update.

OUTPUT:
  output.adoption_packet (plus a route-prompt when delegated application is approved).

LIMITS:
  No product code, no migrating live state into durable files, no visibility/settings changes, no merge/tag/release.
  Preserve target-owned notes, security/domain constraints, and validation commands.


RECOMMENDED_NEXT_OPERATION:
  Terminal agent applies adoption, then Operation 03 (Verify target adoption).
