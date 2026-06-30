# Draftear Route-Prompt para Correcciones de Review

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  Draft a correction route-prompt that delegates fixes to a terminal agent under
  workflow.issue_implementation, mode.delegated_commit_pr.

INPUT:
  ISSUE_NUMBER=<ISSUE_NUMBER>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the original issue, its associated PR, or the feedback cannot be read live.

LIVE_STATE:
  Read the original ISSUE_NUMBER scope, the associated PR diff and changed files, and PM_FEEDBACK_HUMANO live.
  Align the feedback against the current implementation to focus the correction.

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
