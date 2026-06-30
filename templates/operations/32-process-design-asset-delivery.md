# Procesar Entrega de Assets de Diseño

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  Recipient is a Human PM.

INPUT:
  DESIGN_DELIVERY=<DESIGN_DELIVERY>
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.

LIVE_STATE:
  Read live: the provided DESIGN_DELIVERY context and the relevant ISSUE_NUMBER if provided.

DO:
  Analyze the DESIGN_DELIVERY (feedback, links, specs, or decisions).
  Map the delivered design into concrete technical tasks, documentation updates, or new issues.
  Draft a route-prompt to apply the design changes, or a pm_command_bundle to track the new work.

OUTPUT:
  output.route_prompt, output.pm_command_bundle, or output.status_result.

LIMITS:
  Draft only. No mutation. Does not download binary files, create graphic files, or process image generation.

RECOMMENDED_NEXT_OPERATION:
  Terminal Agent executes route_prompt (07) or (08), or Human PM executes pm_command_bundle (04) or (21).
