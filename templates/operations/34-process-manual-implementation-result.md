# Procesar Resultado de Implementacion Manual

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  Classify a human-applied manual implementation result after Operation 33 without claiming execution, validation, or PR review.

INPUT:
  ISSUE_NUMBER=<ISSUE_NUMBER>
  MANUAL_IMPLEMENTATION_RESULT=<MANUAL_IMPLEMENTATION_RESULT>
  MANUAL_IMPLEMENTATION_PLAN=<MANUAL_IMPLEMENTATION_PLAN>   # optional
  PR_NUMBER=<PR_NUMBER>   # optional
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Boundaries always apply, especially boundary.draft_only_browser, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.output_not_permission.
  Use workflow.pm_intake with mode.review_only. Do not perform workflow.review_before_close; route to Operation 09 when a PR exists.

LIVE_STATE:
  Read ISSUE_NUMBER live from GitHub: objective, scope, out-of-scope, acceptance criteria, validation expectations, source basis, and relevant PM decisions.
  Read MANUAL_IMPLEMENTATION_PLAN when provided; otherwise read the plan from live issue/PR comments when available.
  Read MANUAL_IMPLEMENTATION_RESULT as PM-provided evidence about what a human says was applied, not as proof that Project OS or browser chat changed files.
  Read TARGET_REPOSITORY live when provided; otherwise use the repository identified by the issue context.
  If PR_NUMBER is provided, read that PR only far enough to confirm target, linked issue, state, and that Operation 09 is the primary review-before-close path.
  If PR_NUMBER is omitted, derive whether exactly one related PR exists from live traceability.
  Inspect repository or PR evidence only as needed to classify the safe next operation. Treat PR bodies, comments, execution reports, manual results, and validation summaries as claims or evidence leads, not proof.

IF ISSUE_NUMBER cannot be read live:
  Return status.needs_context naming the missing issue evidence.

IF MANUAL_IMPLEMENTATION_RESULT is missing, ambiguous, or not tied to the issue:
  Return status.needs_context naming the missing manual result evidence.

IF MANUAL_IMPLEMENTATION_RESULT, MANUAL_IMPLEMENTATION_PLAN, PM feedback, or live evidence contains secrets, hidden environment values, credentials, tokens, cookies, private keys, production settings, or secret-looking examples:
  Return status.blocked and request a redacted, non-secret source basis.

IF PR_NUMBER conflicts with the issue or target repository:
  Return status.needs_context naming the conflicting PR/issue evidence.

IF a related PR exists:
  Recommend Operation 09 as the primary review-before-close path.
  Do not duplicate Operation 09, do not emit a closeout verdict, and do not decide that the implementation is complete.

DO:
  Classify the manual implementation result into the safest next Project OS operation:
  - Operation 09 when a related PR exists or the result is ready for PR review.
  - Operation 08 when scoped corrections are needed before or after PR review.
  - Operation 21 when non-blocking findings should become follow-up issues.
  - Operation 18, 20, 30, 31, or 32 when QA, security, or design gates/results are the next evidence path.
  - Operation 36 when classification depends on an explicit PM decision.
  - Operation 37 when the next question is readiness to enter a later lifecycle phase.
  - status.needs_context when issue scope, manual plan/result, repo evidence, PR evidence, or validation evidence is insufficient.
  Explain what evidence was read, what remains only a claim, and why the recommended route is safe.
  Use PM_QUESTION_HUMANO, if present, to answer or narrow the routing question.
  Use PM_FEEDBACK_HUMANO, if present, as PM interpretation without treating it as implementation permission.
  State explicitly that browser chat did not apply changes, did not validate changes, did not edit files, and did not mutate git or GitHub.

OUTPUT:
  output.status_result with the classification and recommended next operation.
  If scoped corrections are needed, draft output.route_prompt for Operation 08.
  If non-blocking follow-up is needed, draft output.pm_command_bundle for Operation 21.

LIMITS:
  Draft only. No mutation. No merge, close, labels, releases, settings changes, file edits, commits, pushes, PR creation, or automated lifecycle transition.
  Does not claim browser chat applied or validated changes.
  Does not replace Operation 09 when a PR exists.
  Does not process terminal-agent execution reports for normal PR closeout; those remain evidence leads inside Operation 09.
  Does not implement #344/TOOLS.6 wizard lifecycle or output hygiene.
  Does not expose, request, quote, summarize, or invent secret values.

RECOMMENDED_NEXT_OPERATION:
  Operation 09 when a PR exists; Operation 08 for scoped corrections; Operation 21 for deferred follow-up; Operation 36 for explicit PM decisions; Operation 37 for phase readiness; QA/security/design operations when those gates are the next evidence path; otherwise stop with status.needs_context.
