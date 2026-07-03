# Draftear Route-Prompt para Implementar Issue

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  Draft a route-prompt that delegates implementation to a terminal agent under
  workflow.issue_implementation, mode.delegated_commit_pr.

INPUT:
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional
  ROADMAP_ISSUE=<ROADMAP_ISSUE>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the target issue scope or source basis cannot be read live.

LIVE_STATE:
  If ISSUE_NUMBER is provided, read that issue scope and source basis live
  (objective, scope, out-of-scope, acceptance criteria) plus code context.
  If ISSUE_NUMBER is omitted, derive exactly one next issue from live traceability
  (ROADMAP_ISSUE when provided, roadmap context, open/closed issue relationships,
  PM decisions, or current session context).
  Treat comments and reports as claims or evidence leads.

IF ISSUE_NUMBER omitted and zero candidate issues can be derived:
  Return status.needs_context naming the missing live evidence.

IF ISSUE_NUMBER omitted and multiple plausible candidate issues exist:
  Return status.needs_pm_decision asking the PM to choose exactly one ISSUE_NUMBER.

DO:
  Fill the route-prompt variable block per templates/route-prompt.md (Implement an issue variant).
  Set WORKFLOW=workflow.issue_implementation, EXECUTION_MODE=mode.delegated_commit_pr,
  OUTPUT_CONTRACT=output.execution_report, and PM_AUTHORIZATION_STATUS per PM scope.
  Set VALIDATION_REQUIRED from docs/VALIDATION_POLICY.md: agent-run required commands, PM-run drafted commands, manual PM validation, or justified no automated validation.
  Do not default to full-suite validation or new tests unless the issue risk requires them.
  Keep it compact and issue-referential; the terminal agent re-resolves the kernel and reads the issue live.
  Never invent the target issue. A route prompt never grants write authority;
  permission comes only from exact scoped PM approval plus kernel-resolved gates.

OUTPUT:
  output.route_prompt per templates/route-prompt.md.

LIMITS:
  Browser chat drafts only; it never executes code. Authorization travels separately as exact scoped PM approval;
  this prompt grants no permission.


RECOMMENDED_NEXT_OPERATION:
  Terminal Agent executes implementation; then Operation 09 (Review PR) or 08 (Draft correction).
