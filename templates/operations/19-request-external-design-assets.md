# Solicitar Assets de Diseño Externos

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.design_asset, mode.review_only.
  Recipient is a real graphic/design specialist: a recipient, not an actor surface.

INPUT:
  DESCRIPTION=<DESCRIPTION>
  PM_QUESTION=<PM_QUESTION>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional


KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the source context and design evidence cannot be read.

LIVE_STATE:
  Read live: the issue/PR, target repository context, and PM-provided design evidence for the UI DESCRIPTION.

DO:
  Identify needed assets and constraints: asset type, usage, dimensions, file format, brand/style/product truth,
  accessibility notes, and acceptance criteria.
  Draft an asset prompt/instructions packet for the design recipient. Redact any sensitive value as [REDACTED].

OUTPUT:
  output.asset_prompt that routes the request only.

LIMITS:
  Browser chat drafts only; generates no images and creates no asset files.
  Target product/design truth stays in the target repository or PM-provided evidence; the recipient is not an actor.


RECOMMENDED_NEXT_OPERATION:
  External design delivers assets, then Operation 07 (Draft issue implementation).
