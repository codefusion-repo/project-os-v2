# Analizar Readiness para Release o Tag

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.release_readiness, mode.review_only.

INPUT:
  TAG_NAME=<TAG_NAME>   # optional
  PM_QUESTION=<PM_QUESTION>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional


KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if merged evidence or validation output cannot be read.

LIVE_STATE:
  Read live: last tag, untagged commits, changelog/notes basis, validation output, and open risks.
  Treat reports as claims or evidence leads.

DO:
  Assess whether merged work, validation, and open risks justify a tag or release.
  IF TAG_NAME missing, recommend a version (patch/minor/major) from the evidence and the case.
  Name gaps and risks explicitly; stop before any tag or release action.

OUTPUT:
  output.status_result with the readiness verdict, recommended version when TAG_NAME is missing, and named gaps.

LIMITS:
  Assess only; never create a tag or release. Tags and releases need separate exact PM approval.


RECOMMENDED_NEXT_OPERATION:
  If ready, Operation 13 (Draft release tag) or 24 (Draft GitHub release).
