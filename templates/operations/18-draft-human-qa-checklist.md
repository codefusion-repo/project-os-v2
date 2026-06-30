# Draftear Checklist de QA Humano

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.review_only, mode.review_only.
  Recipient is a human QA tester: not an actor surface and receives no route-prompt.

INPUT:
  ISSUE_NUMBER=<ISSUE_NUMBER>

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the issue requirements and acceptance basis cannot be read.

LIVE_STATE:
  Read live: original requirements, PM acceptance, and key UI/UX changes for ISSUE_NUMBER.

DO:
  Map the technical changes against human usage flows.
  Extract the non-automatable requirements into a copy-ready Markdown checklist.

OUTPUT:
  output.status_result carrying the QA checklist ready to copy or comment on GitHub.

LIMITS:
  Draft only for an external QA recipient (not an actor). No mutation.


RECOMMENDED_NEXT_OPERATION:
  External QA executes checklist, then Operation 09 (Review PR) or 08 (Draft correction).
