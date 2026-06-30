# Draftear Comando Crear Siguiente Issue desde Trazabilidad Viva

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  The drafted issue targets workflow.issue_implementation, mode.delegated_commit_pr execution.

INPUT:
  ROADMAP_ISSUE=<ROADMAP_ISSUE>   # optional
  PM_QUESTION=<PM_QUESTION>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional


KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the live traceability needed to choose the next outcome cannot be read.

LIVE_STATE:
  Reconstruct state live: roadmap (ROADMAP_ISSUE), current code state, PM decisions, fixed docs,
  open issues, and the most recent closed issues. Treat comments and reports as claims or evidence leads.

DO:
  Compare achieved vs planned progress and infer the single next real outcome.
  Shape one issue body per templates/artifacts.md (Issue).
  Draft a copy-safe PM command bundle (templates/pm-command-bundle.md) that runs `gh issue create` with a body file.

IF no single next outcome is derivable from live traceability:
  Return status.needs_pm_decision with the options; do not invent a backlog.

OUTPUT:
  output.pm_command_bundle for exactly one issue the PM runs by hand.

LIMITS:
  Browser chat drafts only. One outcome per issue; never invent issues not grounded in live traceability.


RECOMMENDED_NEXT_OPERATION:
  Human PM executes the bundle, then Operation 07 (Draft issue implementation).
