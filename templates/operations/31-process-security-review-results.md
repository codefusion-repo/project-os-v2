# Procesar Resultados de Revisión de Seguridad

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  Recipient is a Human PM.

INPUT:
  SECURITY_REVIEW_RESULT=<SECURITY_REVIEW_RESULT>
  PR_NUMBER=<PR_NUMBER>   # optional
  PM_QUESTION=<PM_QUESTION>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional


KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the context cannot be read without exposing secrets.

LIVE_STATE:
  Read live: the SECURITY_REVIEW_RESULT.
  If PR_NUMBER is provided, read that PR diff and linked issue.
  If PR_NUMBER is omitted, derive exactly one target PR and linked issue from
  SECURITY_REVIEW_RESULT, live PR/issue traceability, PM decisions, and current
  session context without exposing secrets.

IF PR_NUMBER omitted and no target PR can be derived:
  Return status.needs_context naming the missing PR, issue, or traceability evidence.

IF PR_NUMBER omitted and multiple plausible target PRs or linked issues exist:
  Return status.needs_pm_decision asking the PM to choose exactly one PR_NUMBER.

DO:
  Analyze SECURITY_REVIEW_RESULT.
  Use PM_QUESTION, if present, to clarify the requested routing or answer the PM question before recommending a next operation.
  Use PM_FEEDBACK_HUMANO, if present, as PM interpretation of the security result without treating it as implementation permission.
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
