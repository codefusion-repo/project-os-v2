# MOS-3.2 draft-bounded-issue-set

MOSDLC:
  ID: MOS-3.2
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/29-draft-bounded-roadmap-issues-command.md
  Classification: replacement
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.pm_command_bundle
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Draft a bounded set of implementation issues from live traceability and roadmap evidence with an explicit PM-provided limit.
  Source map summary: Draftea un conjunto acotado de issues desde trazabilidad viva y roadmap. Planificar lotes de trabajo con límite explícito. Exige un límite y draftea un bundle por outcome.

INPUT:
  ROADMAP_ISSUE=<ROADMAP_ISSUE>
  ISSUE_COUNT_LIMIT=<ISSUE_COUNT_LIMIT>   # optional
  SCOPE_LIMIT=<SCOPE_LIMIT>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.copy_safe_commands, boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/29-draft-bounded-roadmap-issues-command.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 29 compatibility template.

LIVE_STATE:
  Read roadmap, open issues, existing issue batches, linked PRs, and PM decisions live before drafting any bundle.
  Require ISSUE_COUNT_LIMIT or SCOPE_LIMIT to keep the batch bounded and one outcome per issue.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Use the explicit ROADMAP_ISSUE plus ISSUE_COUNT_LIMIT or SCOPE_LIMIT to split only bounded outcomes.
  Draft output.pm_command_bundle with one command per issue and no hidden backlog expansion.
  Return status.needs_pm_decision when the limit, priority, or issue boundaries are ambiguous.

OUTPUT:
  output.pm_command_bundle with bounded Human PM-executed issue creation commands, or output.status_result when limits or evidence are insufficient.

LIMITS:
  Draft-only or read-only operation; no file, git, GitHub, settings, release, tag, label, merge, closure, runtime-config, secret-store, product-code, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.4.
