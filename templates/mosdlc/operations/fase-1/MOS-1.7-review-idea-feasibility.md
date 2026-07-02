# MOS-1.7 review-idea-feasibility

MOSDLC:
  ID: MOS-1.7
  Phase: Fase 1 - Requirements, planning, and feasibility
  Surface: actor.browser_chat
  Compatibility source: templates/operations/16-review-idea-as-system-feature.md
  Classification: replacement
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state

OPERATION:
  Review a new idea as a potential project requirement and recommend whether it should enter the roadmap.

INPUT:
  IDEA=<IDEA>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/16-review-idea-as-system-feature.md as the replacement source for idea feasibility review.
  Do not delete, rename, renumber, or bypass the 16 compatibility template.

LIVE_STATE:
  Read IDEA, repository state, roadmap anchors, docs, issues, ADRs, and PM decisions live.
  Treat feasibility recommendations as advisory and read-only.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Evaluate whether the idea fits current requirements, roadmap, constraints, architecture, and known PM decisions.
  Identify duplicates, conflicts, dependencies, risks, and required PM decisions.
  Recommend MOS-1.8 only when the idea is viable enough to document or roadmap.

OUTPUT:
  output.status_result with feasibility diagnosis, evidence read, risks, PM decisions needed, and safe next operation.

LIMITS:
  Read-only review; no issue creation, docs write, roadmap update, file, git, GitHub, settings, release, label, merge, closure, product-code, runtime-config, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-1.8 update-docs-roadmap-with-requirement if the PM accepts the requirement.
