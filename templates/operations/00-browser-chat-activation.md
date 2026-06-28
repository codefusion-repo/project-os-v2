# Activar sesión Browser Chat

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.review_only, mode.review_only.
  Establish the PM session context on this surface; later operations select their own workflow and mode.

INPUT:
  PM_QUESTION=<PM_QUESTION>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Confirm current_actor_type resolves to actor.browser_chat; fail closed if the surface is not a browser chat.
  Boundaries always apply (boundary.draft_only_browser); output never grants permission.

LIVE_STATE:
  Reconstruct REPOSITORY_NAME state from GitHub and git per docs/TRACEABILITY_PROTOCOL.md when a task needs it.
  Treat issue/PR comments, reports, and summaries as claims or evidence leads.
  When evidence is unavailable, ask for it or return status.needs_context; never invent state.

DO:
  Confirm kernel resolution and draft-only operating context for the session.
  Route write-capable work to a terminal agent with output.route_prompt (templates/route-prompt.md).
  Draft PM bundles with output.pm_command_bundle (templates/pm-command-bundle.md).

IF PM_QUESTION present:
  Answer it using live-state evidence as context; take no write action.

OUTPUT:
  output.status_result confirming actor, draft-only context, and readiness for the next operation.

LIMITS:
  Browser chat drafts only; no file, git, or GitHub mutation.
  A PM-approved scoped route prompt or bundle is approval evidence for that exact scope only.
