# MOS-3.16 request-3d-asset

MOSDLC:
  ID: MOS-3.16
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat to external_recipient
  Compatibility source: templates/operations/19-request-external-design-assets.md
  Classification: variant; merge-candidate (con MOS-3.15 vía ASSET_TYPE)
  Workflow: workflow.design_asset
  Mode: mode.review_only
  Output: output.asset_prompt
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Draft an external-recipient asset request prompt without treating the recipient as a kernel actor.
  Source map summary: Draftea el asset prompt para solicitar un asset 3D a un destinatario externo. Obtener assets 3D sin tratar al creador como actor kernel. Prompt PM-facing con objetivo, restricciones y formato de entrega.

INPUT:
  DESCRIPTION=<DESCRIPTION>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.design_asset with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/19-request-external-design-assets.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 19 compatibility template.

LIVE_STATE:
  Read target repository context, product/design truth, issue or feature context, and PM asset constraints live.
  Treat the external recipient as a recipient only, not as a new kernel actor.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft output.asset_prompt with source context, asset objective, asset type, usage context, dimensions, format, accessibility, acceptance criteria, and out-of-scope limits.
  State that target product and design truth stays in repository evidence or PM-provided source basis.
  Do not generate binary assets, create files, upload secrets, or define external recipients as kernel actors.
  ASSET_TYPE is fixed by this template as 3D; do not collapse Fase 3 asset variants unless a separate issue approves it.
  Preserve external-recipient posture; the recipient is not a kernel actor.

OUTPUT:
  output.asset_prompt for an external recipient, or output.status_result when source context is insufficient.

LIMITS:
  Asset prompt drafting only; external recipients are not kernel actors and this template creates no binary assets or repository files.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.20.
