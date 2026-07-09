# Revisar PR antes de Cierre y Draftear Paquete

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.review_before_close, mode.review_only.

INPUT:
  PR_NUMBER=<PR_NUMBER>
  EXECUTION_REPORT=<EXECUTION_REPORT>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if required live evidence cannot be inspected.

LIVE_STATE:
  Read linked issue objective, scope, out-of-scope, and acceptance criteria live.
  Read PR body, comments, changed files, diff, and validation output.
  Read EXECUTION_REPORT when provided directly by the PM, or from GitHub when already present there.
  Open relevant final head files when diff context is insufficient.
  Treat PR body, comments, EXECUTION_REPORT, terminal-agent reports, and validation summaries as claims or evidence leads, not proof.
  When a PR exists, this operation is the standard Project OS path for consuming terminal-agent execution reports before close.

DO:
  Compare implementation behavior and validation against the linked issue requirements and docs/VALIDATION_POLICY.md.
  Compare EXECUTION_REPORT claims against issue scope, PR diff, final head files, and validation evidence.
  Accept scoped PM-run command output, manual PM validation, or a justified no-automated-check exception when broad agent-run validation was intentionally out of scope.
  Fail closed when mandatory validation is missing for kernel, resolver, security, authorization, traceability, deployment, secret-sensitive, production-impacting, or deterministic contract changes.
  Never emit GO/resolved based only on EXECUTION_REPORT, PR body, comments, or validation summary claims.
  Verify scope, out-of-scope, secret-safety, and acceptance criteria against code/diff/final-file evidence.
  Return output.review_result with verdict and findings.

IF code/diff/final-file evidence cannot be inspected:
  Return status.needs_context. Do not return GO/resolved.

IF verdict == resolved:
  Draft closeout package:
    - IF ISSUE/PR lacks REVIEW_RESULT, EXECUTION_REPORT, CORRECTION_REPORT, PM_DECISION, or CLOSURE_COMMENT on GitHub, include or summarize the provided EXECUTION_REPORT as an evidence lead and draft the appropriate GitHub comment command.
    - IF PR is not ready, draft READY command.
    - IF PR is not merged, draft MERGE command.
    - IF issue is not closed, draft CLOSE command.
    - IF remote issue branch exists, draft CLEANUP_REMOTO.
    - ALWAYS draft CLEANUP_LOCAL.

IF verdict != resolved:
  Do not draft closeout package. Report findings only.

OUTPUT:
  output.review_result.
  If verdict == resolved, also draft output.pm_command_bundle for the PM closeout package (templates/pm-command-bundle.md).

LIMITS:
  Browser chat drafts only. Human PM executes merge, close, tag, release, comments, and cleanup commands.
  Do not mutate GitHub or repo from browser_chat.
  Do not route a normal PR execution report to a separate processor; inspect it here as evidence lead for review-before-close.
  Do not emit GO based only on EXECUTION_REPORT.


RECOMMENDED_NEXT_OPERATION:
  If resolved, Operation 10 (Draft PR closeout). If gaps remain, Operation 08 (Draft correction).
