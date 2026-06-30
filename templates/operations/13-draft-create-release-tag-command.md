# Draftear Comando para Crear Release Tag

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.release_readiness, mode.review_only.

INPUT:
  TAG_NAME=<TAG_NAME>   # optional
  PM_QUESTION=<PM_QUESTION>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional


KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if repo state or validation output cannot be read.

LIVE_STATE:
  Read live: readiness evidence, existing tags, and the current default-branch head.
  Treat reports as claims or evidence leads.

DO:
  Confirm TAG_NAME does not collide with existing tags and is coherent with the readiness verdict.
  Draft a copy-safe PM command bundle (templates/pm-command-bundle.md) with `git tag` and `git push --tags`.

IF TAG_NAME missing:
  Stop at the readiness recommendation. Do not emit the final execution commands.

OUTPUT:
  output.pm_command_bundle the Human PM runs and authorizes.

LIMITS:
  Browser chat drafts only; agents never create tags. Tag execution is the Human PM's exclusive authority.


RECOMMENDED_NEXT_OPERATION:
  Human PM executes the bundle.
