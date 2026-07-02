# MOS-3.9 verify-post-merge

MOSDLC:
  ID: MOS-3.9
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat / actor.terminal_agent
  Compatibility source: templates/operations/11-verify-post-merge-state.md
  Classification: replacement
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state

OPERATION:
  Verify post-merge repository and issue state without mutating GitHub or git.
  Source map summary: Verifica que la rama principal quedó saludable y el issue resuelto tras el merge. Cerrar el loop de implementación con evidencia. Chequeo read-only de default branch, issue y checks.

INPUT:
  PR_NUMBER=<PR_NUMBER>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/11-verify-post-merge-state.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 11 compatibility template.

LIVE_STATE:
  Read default branch state, issue state, PR state, checks, and relevant validation evidence live after the Human PM merge.
  Treat verification as read-only sanity checking, not as closure authority.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Check that default branch, linked issue, merged PR state, and relevant validation evidence are consistent after merge.
  Report drift, missing closure evidence, or post-merge failures with the safe next operation.
  Do not reopen, close, label, comment, reset branches, or run release actions.

OUTPUT:
  output.status_result with post-merge verification findings, missing evidence, risks, and safe next operation.

LIMITS:
  Draft-only or read-only operation; no file, git, GitHub, settings, release, tag, label, merge, closure, runtime-config, secret-store, product-code, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.1.
