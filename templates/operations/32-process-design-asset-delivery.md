# Procesar Entrega de Assets de Diseño

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  Recipient is a Human PM.

INPUT:
  DESIGN_DELIVERY=<DESIGN_DELIVERY>
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional
  PM_QUESTION=<PM_QUESTION>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional


KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.

LIVE_STATE:
  Read live: the provided DESIGN_DELIVERY context.
  If ISSUE_NUMBER is provided, use that issue as the target evidence basis.
  If ISSUE_NUMBER is omitted, derive exactly one target issue from DESIGN_DELIVERY,
  live traceability, PM decisions, and current session context.

IF ISSUE_NUMBER omitted and no target issue can be derived:
  Return status.needs_context naming the missing issue or traceability evidence.

IF ISSUE_NUMBER omitted and multiple plausible target issues or product routes exist:
  Return status.needs_pm_decision asking the PM to choose exactly one ISSUE_NUMBER
  or decide whether the delivery should become implementation, correction,
  documentation, or follow-up work.

DO:
  Analyze the DESIGN_DELIVERY (feedback, links, specs, or decisions).
  Use PM_QUESTION, if present, to clarify whether the delivery should become implementation, documentation, correction, or follow-up work.
  Use PM_FEEDBACK_HUMANO, if present, as PM interpretation of the delivery without treating it as implementation permission.
  Map the delivered design into concrete technical tasks, documentation updates, or new issues.
  Draft a route-prompt to apply the design changes, or a pm_command_bundle to track the new work.

OUTPUT:
  output.route_prompt, output.pm_command_bundle, or output.status_result.

LIMITS:
  Draft only. No mutation. Does not download binary files, create graphic files, or process image generation.

RECOMMENDED_NEXT_OPERATION:
  Terminal Agent executes route_prompt (07) or (08), or Human PM executes pm_command_bundle (04) or (21).
