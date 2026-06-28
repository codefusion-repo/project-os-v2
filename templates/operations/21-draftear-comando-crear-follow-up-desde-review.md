# Draftear Comando Crear Follow Up desde Review

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  The drafted follow-up issue targets workflow.issue_implementation execution later.

INPUT:
  PR_NUMBER=<PR_NUMBER>

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the review findings and source basis cannot be read.

LIVE_STATE:
  Read live: PR_NUMBER review findings, incomplete reviews, and out-of-scope notes.

DO:
  Distinguish a blocking finding (immediate correction) from a deferred one (follow-up).
  Shape one deferred issue body per templates/artifacts.md (Issue).
  Draft a copy-safe PM command bundle (templates/pm-command-bundle.md) that runs `gh issue create` with a body file.

OUTPUT:
  output.pm_command_bundle for the new follow-up issue, without stopping the current merge.

LIMITS:
  Browser chat drafts only. Do not assume security problems may be deferred or ignored.
