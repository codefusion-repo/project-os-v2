# Procesar Resultados de QA Humano

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  Recipient is a Human PM.

INPUT:
  QA_RESULT=<QA_RESULT>
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional
  PM_QUESTION=<PM_QUESTION>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional


KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the original requirements and acceptance basis cannot be read.

LIVE_STATE:
  Read live: the QA_RESULT, original requirements, and PM acceptance for ISSUE_NUMBER if provided.

DO:
  Analyze QA_RESULT against the original requirements and PM acceptance.
  Use PM_QUESTION, if present, to clarify the requested routing or answer the PM question before recommending a next operation.
  Use PM_FEEDBACK_HUMANO, if present, as PM interpretation of the QA result without treating it as implementation permission.
  Identify if there are blocking failures, non-blocking defects, or if the QA passed.
  If there are blocking failures, draft a route-prompt for the terminal agent to correct them.
  If there are non-blocking defects, draft a pm_command_bundle to create follow-up issues.
  If QA passed, return status.resolved.

OUTPUT:
  output.route_prompt, output.pm_command_bundle, or output.status_result.

LIMITS:
  Draft only. No mutation. Does not execute PR closure, merge, or external QA testing.

RECOMMENDED_NEXT_OPERATION:
  Terminal Agent executes route_prompt (08), or Human PM executes pm_command_bundle (21), or PR Review (09).
