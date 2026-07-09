# MOS-2.7 inventory-design-docs

MOSDLC:
  ID: MOS-2.7
  Phase: Fase 2 - Design
  Surface: actor.browser_chat
  Compatibility source: none
  Classification: new
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state, evidence.target_adoption

OPERATION:
  Inventory existing design documentation in an adopted target project before creating or updating Fase 2 docs.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  This is a new MOSDLC operation with no direct 00-37 compatibility source.
  Do not delete, rename, renumber, or bypass any 00-37 compatibility template.

LIVE_STATE:
  Read target adoption evidence, repository docs, ADRs, design assets, and PM decisions live.
  Treat the inventory as a point-in-time report, not durable project state.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Identify existing architecture, UI/UX, data/algorithm, coding standards, and security design docs.
  Note stale, missing, duplicated, or ambiguous design sources without editing files.
  Return status.needs_context when target adoption or repository evidence cannot be inspected.

OUTPUT:
  output.status_result with the inventory, evidence gaps, PM decisions needed, and safe next operation.

LIMITS:
  Read-only inventory; no file, git, GitHub, settings, release, label, merge, closure, product-code, runtime-config, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-2.8 audit-design-doc-gaps.
