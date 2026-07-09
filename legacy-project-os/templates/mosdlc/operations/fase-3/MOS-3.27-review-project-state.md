# MOS-3.27 review-project-state

MOSDLC:
  ID: MOS-3.27
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat
  Compatibility source: templates/operations/05-review-project-state-and-misalignment.md
  Classification: replacement
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state

OPERATION:
  Review project state and documentation alignment from live repository and PM decision evidence.
  Source map summary: Revisa estado del proyecto y desalineaciones respecto a la documentación. Detectar drift entre docs, roadmap y realidad del repo. Usa decisiones PM y docs fijos como verdad principal.

INPUT:
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/05-review-project-state-and-misalignment.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 05 compatibility template.

LIVE_STATE:
  Read durable docs, roadmap, ADRs, issues, PRs, repository state, and PM decisions live.
  Use PM decisions and stable docs as the primary truth for identifying drift or misalignment.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Compare current repository, roadmap, docs, issues, and PR state against stable PM decisions and source docs.
  Identify drift, stale assumptions, missing traceability, or needed next operation with evidence anchors.
  Remain read-only and return status.needs_context or status.needs_pm_decision when the state cannot support a single safe recommendation.

OUTPUT:
  output.status_result with drift, missing evidence, PM decisions needed, and safe next operation.

LIMITS:
  Draft-only or read-only operation; no file, git, GitHub, settings, release, tag, label, merge, closure, runtime-config, secret-store, product-code, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-R.9.
