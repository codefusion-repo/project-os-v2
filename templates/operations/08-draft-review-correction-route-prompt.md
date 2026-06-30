# Draftear Route-Prompt para Correcciones de Review

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  Draft a correction route-prompt that delegates fixes to a terminal agent under
  workflow.issue_implementation, mode.delegated_commit_pr.

INPUT:
  ISSUE_NUMBER=<ISSUE_NUMBER>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the original issue, its associated PR, and at least one actionable correction basis cannot be read live.

LIVE_STATE:
  Read the original ISSUE_NUMBER scope, the associated PR diff and changed files, and PM_FEEDBACK_HUMANO when provided.
  Align PM_FEEDBACK_HUMANO and any live review findings against the current implementation to focus the correction.

IF PM_FEEDBACK_HUMANO omitted and no actionable live review finding exists:
  Return status.needs_context naming the missing feedback or review evidence.

IF PM_QUESTION_HUMANO present:
  Answer it using live issue/PR evidence before drafting the correction route.

DO:
  Fill the route-prompt variable block per templates/route-prompt.md (Apply review corrections variant).
  List findings as `file:line — finding`; keep SCOPE to the same branch and the same issue scope.
  Set PM_AUTHORIZATION_STATUS per PM scope.

OUTPUT:
  output.route_prompt (copy-safe) for the scoped correction.

LIMITS:
  Browser chat drafts only. Do not re-implement the whole issue or expand the task scope.


RECOMMENDED_NEXT_OPERATION:
  Terminal Agent executes correction; then Operation 09 (Review PR before close).
