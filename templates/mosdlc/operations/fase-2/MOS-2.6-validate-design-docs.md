# MOS-2.6 validate-design-docs

MOSDLC:
  ID: MOS-2.6
  Phase: Fase 2 - Design
  Surface: actor.browser_chat
  Compatibility source: none
  Classification: new
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.source_basis, evidence.repo_state

OPERATION:
  Validate design documentation against Fase 1 requirements before implementation planning.

INPUT:
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
  Read Fase 1 requirements, design docs, ADRs, issues, and repository evidence live.
  Treat design docs as source basis to review, not as proof that implementation state is complete.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Check coverage, contradictions, missing design areas, unclear architecture or UI/UX choices, security gaps, and unresolved PM decisions.
  Report actionable gaps with evidence anchors and the safe next operation.
  Return status.needs_context when the source docs or requirement source basis cannot be inspected.

OUTPUT:
  output.status_result with validation findings, missing evidence, PM decisions needed, and safe next operation.

LIMITS:
  Read-only validation; no file, git, GitHub, settings, release, label, merge, closure, product-code, runtime-config, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-R.4 review-phase-readiness, then MOS-3.1 when ready.
