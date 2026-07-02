# MOS-1.10 extract-requirements-from-existing

MOSDLC:
  ID: MOS-1.10
  Phase: Fase 1 - Requirements, planning, and feasibility
  Surface: actor.browser_chat
  Compatibility source: none
  Classification: new
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state, evidence.target_adoption

OPERATION:
  Identify observable requirements from an existing adopted project that lacks formal Fase 1 documentation.

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
  Read TARGET_REPOSITORY adoption evidence, docs, README, code structure, tests, issues, ADRs, and roadmap anchors live.
  Treat inferred requirements as observable evidence needing PM validation, not as final product scope.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Extract functional requirements, non-functional requirements, constraints, user roles, workflows, and open questions from observable project evidence.
  Separate confirmed evidence from inference and PM assumptions.
  Return status.needs_context when target adoption or repository evidence cannot be inspected.

OUTPUT:
  output.status_result with extracted requirements, evidence anchors, inference notes, open questions, and safe next operation.

LIMITS:
  Read-only extraction; no file, git, GitHub, settings, release, label, merge, closure, product-code, runtime-config, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-1.11 update-requirements-docs-existing.
