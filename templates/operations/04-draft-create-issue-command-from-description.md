# Draftear Comando Crear Issue desde Descripción

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  The drafted issue targets workflow.issue_implementation, mode.delegated_commit_pr execution.

INPUT:
  DESCRIPTION=<DESCRIPTION>

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if DESCRIPTION lacks enough source basis for an actionable issue.

LIVE_STATE:
  Read DESCRIPTION and the live source basis it builds on (prior issues, PRs, ADRs, decisions).

DO:
  Shape one actionable issue body per templates/artifacts.md (Issue): one outcome, scope, out-of-scope,
  acceptance criteria, validation expectations, and risk/rollback.
  Draft a copy-safe PM command bundle (templates/pm-command-bundle.md) that runs `gh issue create` with a body file.

OUTPUT:
  output.pm_command_bundle the PM runs by hand.

LIMITS:
  Browser chat drafts only; the PM executes the bundle. One outcome per issue; body under ~5KB.


RECOMMENDED_NEXT_OPERATION:
  Human PM executes the bundle, then Operation 07 (Draft issue implementation).
