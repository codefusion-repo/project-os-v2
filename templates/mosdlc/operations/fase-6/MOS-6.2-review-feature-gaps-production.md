# MOS-6.2 review-feature-gaps-production

MOSDLC:
  ID: MOS-6.2
  Phase: Fase 6 - Maintenance and tooling
  Surface: actor.browser_chat
  Compatibility source: none
  Classification: new
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Review functional feature gaps for production readiness.
  Source map summary: Revisa gaps de funcionalidades para production readiness. Saber qué falta funcionalmente antes de producción. Contrasta features reales contra docs y requisitos.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only and emit only the declared output contracts.
  Apply boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  This is a new MOSDLC operation with no direct 00-37 compatibility source.
  Do not delete, rename, renumber, or bypass any 00-37 compatibility template.

LIVE_STATE:
  Read TARGET_REPOSITORY requirements docs, roadmap, and observable implemented behavior live.
  Treat gap findings as advisory input to the PM's production-readiness decision.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Contrast documented requirements, use cases, and user stories against the code's observable behavior.
  Identify missing, partial, or divergent functionality with concrete file or doc references.
  Classify each gap as blocking or non-blocking for production readiness.
  Return status.needs_context when requirements docs or repository evidence cannot be inspected.
  Do not implement missing functionality, edit files, or claim feature parity is complete.

OUTPUT:
  output.status_result carrying the feature-gap findings, blocking classification, and safe recommended next operation.

LIMITS:
  Read-only feature-gap review; no repository, GitHub, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-6.8.
