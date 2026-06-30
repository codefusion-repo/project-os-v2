# Verificar Estado Post-Merge

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.review_only, mode.review_only.
  A terminal agent may run this read-only against a local checkout.

INPUT:
  PR_NUMBER=<PR_NUMBER>
  PM_QUESTION=<PM_QUESTION>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional


KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the live repo/issue state cannot be read.

LIVE_STATE:
  Read live: default-branch state and latest commits, the linked issue status, and CI/checks for the merge.
  Treat reports as claims or evidence leads.

DO:
  Confirm the default branch is healthy after merge and the linked issue resolved.
  Name any breakage, unintended files, or issue references that did not close.

OUTPUT:
  output.status_result with the post-merge sanity findings; no fixes applied.

LIMITS:
  Read-only verification; report only, do not fix. No file, git, or GitHub mutation.


RECOMMENDED_NEXT_OPERATION:
  Operation 06 (Draft next issue) or 12 (Analyze release readiness).
