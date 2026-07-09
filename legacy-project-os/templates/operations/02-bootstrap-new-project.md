# Iniciar Bootstrap de Nuevo Proyecto

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.target_adoption, mode.review_only.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  DESCRIPTION=<DESCRIPTION>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if target identity or required adoption evidence is missing or ambiguous.

LIVE_STATE:
  Read the new TARGET_REPOSITORY state live and any PM-provided initial intent.
  Confirm whether adoption files already exist; do not assume a terminal agent is configured before adoption.

DO:
  Draft the initial adoption structure: canonical adapters filled for the target and a foundational roadmap-issue draft.
  Draft an adoption checklist for the PM.

OUTPUT:
  output.adoption_packet with adapter drafts, the foundational roadmap-issue draft, and the checklist.

LIMITS:
  Review/draft only on this surface; no file, git, or GitHub mutation.
  No product code, settings, or kernel rewrite; product truth stays in the target repository.


RECOMMENDED_NEXT_OPERATION:
  Operation 03 (Verify target adoption).
