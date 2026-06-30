# Draftear Roadmap desde Docs

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  Draft a roadmap issue body or PM command bundle from stable docs and source basis.

INPUT:
  SOURCE_DOCS=<SOURCE_DOCS>
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  ROADMAP_ACTION=<create|update>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Required evidence: evidence.source_basis and evidence.repo_state.
  Fail closed if SOURCE_DOCS or the cited source basis cannot be read or conflicts with explicit PM decisions.

LIVE_STATE:
  Read SOURCE_DOCS, linked issues/PRs/ADRs, existing roadmap issue when present, and PM decisions live.
  Treat docs as stable source basis, not as proof of current issue/PR completion state.
  Use PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO, when provided, only to interpret roadmap direction or surface PM choices.

DO:
  Convert stable direction into one roadmap issue body per templates/artifacts.md (Roadmap issue).
  Preserve fixed decisions, phases, kill criteria, not-now scope, and non-authorization language.
  IF ROADMAP_ACTION=create, draft a copy-safe PM command bundle (templates/pm-command-bundle.md) for `gh issue create`.
  IF ROADMAP_ACTION=update, draft the proposed roadmap body/update text and the PM command bundle only when exact
  repository and issue targets are known.
  Surface conflicts or missing PM choices instead of inventing roadmap priority.

IF the docs imply implementation issues rather than a roadmap:
  Return status.needs_pm_decision naming whether to use the bounded roadmap-to-issues operation instead.

OUTPUT:
  output.draft_issue for the roadmap body, or output.pm_command_bundle when the PM asks for a copy-safe create/update bundle.
  output.status_result when source basis, live roadmap evidence, or PM decisions are missing.

LIMITS:
  Browser chat drafts only; the PM executes GitHub writes. Do not store live progress state in the roadmap body.


RECOMMENDED_NEXT_OPERATION:
  Human PM executes the bundle, then Operation 06 or 29.
