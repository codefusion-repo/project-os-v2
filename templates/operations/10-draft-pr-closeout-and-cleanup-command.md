# Draftear Comando Cierre de PR y Limpieza

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.review_before_close, mode.review_only.

INPUT:
  PR_NUMBER=<PR_NUMBER>
  ISSUE_NUMBER=<ISSUE_NUMBER>

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if issue scope, PR diff, validation output, or live PR/issue state cannot be inspected.
  A drafted closeout never substitutes for code-backed review-before-close.

LIVE_STATE:
  Read issue scope, PR diff and changed files, validation output, and live PR/issue state on GitHub.
  Treat comments and reports as claims or evidence leads.

DO:
  Determine, from live state, which closeout pieces are missing, then draft the common closeout bundle
  per templates/pm-command-bundle.md (Closeout):
    - comment commands for missing pieces (REVIEW_RESULT / EXECUTION_REPORT / CORRECTION_REPORT / PM_DECISION / CLOSURE_COMMENT) when applicable;
    - READY command if the PR is still a draft;
    - MERGE command if the PR is not merged;
    - CLOSE command if the issue is not closed;
    - CLEANUP_REMOTO if the remote issue branch exists;
    - CLEANUP_LOCAL always.

OUTPUT:
  output.pm_command_bundle the Human PM runs by hand.

LIMITS:
  Browser chat drafts only; it never executes merge/close/cleanup. The Human PM executes the bundle.


RECOMMENDED_NEXT_OPERATION:
  Human PM executes the bundle, then Operation 11 (Verify post-merge state).
