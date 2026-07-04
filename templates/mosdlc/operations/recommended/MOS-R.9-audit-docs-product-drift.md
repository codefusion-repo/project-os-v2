# MOS-R.9 audit-docs-product-drift

MOSDLC:
  ID: MOS-R.9
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat
  Compatibility source: templates/operations/05-review-project-state-and-misalignment.md
  Classification: accepted-recommended; variant (drift documental explícito)
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Audit drift between the target project's documentation and its real product behavior, read-only.
  Source map summary: Audita drift entre documentación y producto real. Mantener docs como verdad usable del producto. Contrasta docs contra código y estado vivo; lista drift accionable.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/05-review-project-state-and-misalignment.md as compatibility source for this recommended operation shape.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read the target repository's documentation, code, and live traceability at execution time; treat documentation claims as claims until the code confirms them.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Read-only comparison of documentation against product code and live state, listing actionable drift items with the evidence for each.
  Classify each drift item as documentation-side (docs must change) or product-side (behavior diverged from agreed docs).
  Return status.needs_context when docs or code evidence cannot be read.
  Do not edit docs or code, create issues, or claim completeness of the audit.

OUTPUT:
  output.status_result with the actionable drift list, per-item classification and evidence, and the recommended correction side.

LIMITS:
  Read-only audit; doc updates and product corrections are separate operations with their own gates.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-1.8 when the drift is documentation-side; MOS-3.3 for product-side follow-ups.
