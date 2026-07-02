# MOS-1.9 review-requirement-removal

MOSDLC:
  ID: MOS-1.9
  Phase: Fase 1 - Requirements, planning, and feasibility
  Surface: actor.browser_chat
  Compatibility source: none
  Classification: new
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.source_basis, evidence.repo_state

OPERATION:
  Review the impact of removing a requirement before docs, roadmap, or implementation work changes.

INPUT:
  DESCRIPTION=<DESCRIPTION>
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
  Read the removal description, requirements docs, roadmap anchors, linked issues, ADRs, repository evidence, and PM decisions live.
  Treat the review as impact analysis, not as authorization to remove docs, issues, code, or roadmap entries.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Identify affected docs, roadmap outcomes, issues, dependencies, acceptance criteria, and risks.
  Return status.needs_pm_decision when removal needs a PM decision or conflicts with durable decisions.
  Recommend MOS-1.8 only when the PM confirms the removal should be reflected in docs or roadmap.

OUTPUT:
  output.status_result with impact analysis, evidence read, required PM decision, and safe next operation.

LIMITS:
  Read-only review; no file, git, GitHub, settings, release, label, merge, closure, product-code, runtime-config, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-1.8 if the PM confirms the requirement removal should update docs or roadmap.
