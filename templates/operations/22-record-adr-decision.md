# Registrar Decisión Arquitectural (ADR)

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  Browser chat drafts; writing the ADR file is delegated to a terminal agent via route-prompt under
  mode.delegated_commit_pr with exact PM approval.

INPUT:
  DECISION=<DECISION>

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the decision context and source basis cannot be read.

LIVE_STATE:
  Read live: the issue discussion and the technical DECISION taken by the PM/team.

DO:
  Formalize context, alternatives, and the rationale for the chosen solution into ADR content per templates/artifacts.md.
  IF the PM decides to write the file, draft a route-prompt (templates/route-prompt.md) that delegates ADR file creation.

OUTPUT:
  output.route_prompt for the ADR file write (alongside the drafted ADR content).

LIMITS:
  Browser chat writes no files. Use only for perennial design decisions, never to store live state.
  The ADR file write requires route-prompt + mode.delegated_commit_pr + exact PM approval.
