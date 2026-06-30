# Procesar Resultados de Revisión de Seguridad

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  Recipient is a Human PM.

INPUT:
  SECURITY_RESULTS=<SECURITY_RESULTS>
  SECURITY_REVIEW_RESULT=<SECURITY_REVIEW_RESULT>   # optional
  PR_NUMBER=<PR_NUMBER>   # optional
  PM_QUESTION=<PM_QUESTION>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  SECURITY_REVIEW_RESULT=<SECURITY_REVIEW_RESULT>   # optional


KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the context cannot be read without exposing secrets.

LIVE_STATE:
  Read live: the SECURITY_RESULTS and the PR_NUMBER diff if provided.

DO:
  Analyze the SECURITY_RESULTS.
  Identify if there are blocking security vulnerabilities or non-blocking recommendations.
  If there are blocking vulnerabilities, draft a route-prompt for the terminal agent to correct them.
  If there are non-blocking recommendations, draft a pm_command_bundle to create follow-up issues.
  If no issues, return status.resolved.

OUTPUT:
  output.route_prompt, output.pm_command_bundle, or output.status_result.

LIMITS:
  Never ask anyone to print, paste, upload, quote, summarize, or expose secrets.
  Draft only. No mutation.

RECOMMENDED_NEXT_OPERATION:
  Terminal Agent executes route_prompt (08), or Human PM executes pm_command_bundle (21), or PR Review (09).
