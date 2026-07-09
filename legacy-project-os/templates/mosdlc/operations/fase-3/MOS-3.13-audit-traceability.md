# MOS-3.13 audit-traceability

MOSDLC:
  ID: MOS-3.13
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat / actor.terminal_agent
  Compatibility source: templates/operations/15-audit-issue-pr-traceability.md
  Classification: replacement
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state

OPERATION:
  Audit live issue and PR traceability to confirm the implementation cycle is reconstructible from evidence.
  Source map summary: Audita issue/PR y trazabilidad viva en GitHub. Verificar que el ciclo es reconstruible desde evidencia. Auditoría read-only de vínculos, evidencia de cierre y estado.

INPUT:
  ISSUE_NUMBER=<ISSUE_NUMBER>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/15-audit-issue-pr-traceability.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 15 compatibility template.

LIVE_STATE:
  Read issue, PRs, commits, comments, validation evidence, roadmap links, and closure evidence live.
  Audit reconstructability without editing issue links, comments, labels, branches, or files.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Check whether issue, PRs, commits, comments, review, validation, and closure evidence reconstruct the work accurately.
  Report gaps as evidence-backed findings and recommend MOS-3.14 to process them.
  Return status.needs_context when the traceability anchor cannot be inspected live.

OUTPUT:
  output.status_result with traceability findings, missing evidence, and safe next operation.

LIMITS:
  Draft-only or read-only operation; no file, git, GitHub, settings, release, tag, label, merge, closure, runtime-config, secret-store, product-code, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.14.
