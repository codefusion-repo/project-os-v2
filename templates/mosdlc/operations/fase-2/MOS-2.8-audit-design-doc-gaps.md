# MOS-2.8 audit-design-doc-gaps

MOSDLC:
  ID: MOS-2.8
  Phase: Fase 2 - Design
  Surface: actor.browser_chat
  Compatibility source: templates/operations/05-review-project-state-and-misalignment.md
  Classification: variant (gap de diseño, no desalineación general)
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Audit gaps between existing design documentation and Fase 1 requirements.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/05-review-project-state-and-misalignment.md as a compatibility reference for evidence-backed gap analysis shape.
  Do not delete, rename, renumber, or bypass the 05 compatibility template.

LIVE_STATE:
  Read existing design docs, Fase 1 requirements, target repository evidence, ADRs, issues, and PM decisions live.
  Treat the gap audit as an advisory report, not an authorization to update files.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Compare current design docs against Fase 1 requirements and classify missing, stale, contradictory, or under-specified design areas.
  Recommend the single safest update operation for the primary gap, or name multiple gaps when PM decision is needed.
  Return status.needs_context when requirements or target docs cannot be inspected.

OUTPUT:
  output.status_result with evidence-backed design gaps, missing context, PM decisions needed, and safe next operation.

LIMITS:
  Read-only audit; no file, git, GitHub, settings, release, label, merge, closure, product-code, runtime-config, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-2.9 through MOS-2.13 according to the primary design gap.
