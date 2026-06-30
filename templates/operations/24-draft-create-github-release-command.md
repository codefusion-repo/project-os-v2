# Draftear Comando para Crear Release de GitHub

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.release_readiness, mode.review_only.

INPUT:
  TAG_NAME=<TAG_NAME>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if repo state or validation output cannot be read.

LIVE_STATE:
  Read live: prior readiness evidence, the last tag/release, commits since the last release, candidate notes, and validation.

DO:
  Confirm TAG_NAME exists or is recommended and that notes reflect the merged outcomes; avoid collision with existing releases.
  Draft a copy-safe PM command bundle (templates/pm-command-bundle.md) that runs `gh release create` (a GitHub Release
  object: notes + tag), distinct from the plain git tag of operation 13.

IF TAG_NAME missing:
  Stop at the readiness-derived recommendation. Do not emit the final publish command.

OUTPUT:
  output.pm_command_bundle the Human PM runs and authorizes.

LIMITS:
  Browser chat drafts only; the Human PM executes and authorizes publication. Publishes no release and tags nothing on its own.


RECOMMENDED_NEXT_OPERATION:
  Human PM executes the bundle.
