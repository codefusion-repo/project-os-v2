# Draftear Route-Prompt para Implementar Issue

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  Draft a route-prompt that delegates implementation to a terminal agent under
  workflow.issue_implementation, mode.delegated_commit_pr.

INPUT:
  ISSUE_NUMBER=<ISSUE_NUMBER>
  ROADMAP_ISSUE=<ROADMAP_ISSUE>   # optional: anchor when deriving the next issue from live traceability

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the issue scope or source basis cannot be read live.

LIVE_STATE:
  Read ISSUE_NUMBER scope and source basis live (objective, scope, out-of-scope, acceptance criteria) plus code context.
  Treat comments and reports as claims or evidence leads.

DO:
  Fill the route-prompt variable block per templates/route-prompt.md (Implement an issue variant).
  Set WORKFLOW=workflow.issue_implementation, EXECUTION_MODE=mode.delegated_commit_pr,
  OUTPUT_CONTRACT=output.execution_report, and PM_AUTHORIZATION_STATUS per PM scope.
  Keep it compact and issue-referential; the terminal agent re-resolves the kernel and reads the issue live.

IF ISSUE_NUMBER not provided:
  Derive the single next issue from live traceability (roadmap, open/closed issues, PM decisions) before drafting.

OUTPUT:
  output.route_prompt per templates/route-prompt.md.

LIMITS:
  Browser chat drafts only; it never executes code. Authorization travels separately as exact scoped PM approval;
  this prompt grants no permission.
