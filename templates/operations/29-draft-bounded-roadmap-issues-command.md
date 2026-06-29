# Draftear Issues Acotados desde Roadmap

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.pm_intake, mode.review_only.
  Draft a bounded set of issue-create bundles from a roadmap while preserving one issue per outcome.

INPUT:
  ROADMAP_ISSUE=<ROADMAP_ISSUE>
  ISSUE_COUNT_LIMIT=<ISSUE_COUNT_LIMIT> optional
  SCOPE_LIMIT=<SCOPE_LIMIT> optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Required evidence: evidence.source_basis and evidence.repo_state.
  Fail closed if the roadmap, live traceability, or explicit bound cannot be read.

LIVE_STATE:
  Read ROADMAP_ISSUE, current open/closed issues, PRs, comments, PM decisions, and fixed docs live.
  Treat roadmap text as direction; derive current gaps from live traceability.

DO:
  Require at least one explicit bound: ISSUE_COUNT_LIMIT or SCOPE_LIMIT.
  Select only the next bounded outcomes supported by the roadmap and live state.
  Shape each outcome as a separate issue body per templates/artifacts.md (Issue).
  Draft one copy-safe PM command bundle (templates/pm-command-bundle.md) with one `gh issue create`
  command per outcome, each using its own body file.
  Preserve operation 06 for the single-next-issue case; do not replace it with batch behavior.

IF neither ISSUE_COUNT_LIMIT nor SCOPE_LIMIT is provided:
  Return status.needs_pm_decision requesting one explicit bound before drafting issues.

IF a candidate outcome is too broad:
  Split it or skip it with a note; never create an issue that bundles multiple outcomes.

OUTPUT:
  output.pm_command_bundle for the bounded set of issue-create commands the PM runs by hand.
  output.status_result when live traceability or explicit bounds are missing.

LIMITS:
  Browser chat drafts only. One issue per outcome; never invent backlog beyond ROADMAP_ISSUE and live traceability.
