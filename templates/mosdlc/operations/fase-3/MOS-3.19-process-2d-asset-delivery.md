# MOS-3.19 process-2d-asset-delivery

MOSDLC:
  ID: MOS-3.19
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/32-process-design-asset-delivery.md
  Classification: variant; merge-candidate (con MOS-3.20 a MOS-3.22 vía ASSET_TYPE)
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.pm_command_bundle, output.route_prompt, output.status_result
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Process delivered asset material or feedback into implementation, correction, or follow-up routing.
  Source map summary: Procesa la entrega de un asset 2D y la mapea a tareas técnicas o drafts. Integrar assets recibidos al ciclo de desarrollo. Clasifica la entrega hacia issue, corrección o follow-up.

INPUT:
  DESIGN_DELIVERY=<DESIGN_DELIVERY>
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/32-process-design-asset-delivery.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 32 compatibility template.

LIVE_STATE:
  Read DESIGN_DELIVERY, asset request context, related issue or feature, repository constraints, and PM decisions live.
  Treat delivered assets as PM-provided source basis until a separate write-capable route applies them.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Classify DESIGN_DELIVERY into implementation route, correction route, follow-up issue, or no-op based on live product context.
  Draft output.route_prompt or output.pm_command_bundle only when the route and target are exact.
  Do not write assets into the repository or claim acceptance without separate PM approval and validation path.
  ASSET_TYPE is fixed by this template as 2D; do not collapse Fase 3 asset variants unless a separate issue approves it.

OUTPUT:
  output.status_result plus output.route_prompt or output.pm_command_bundle only when delivery classification selects that draft path.

LIMITS:
  Asset delivery processing only; applying assets to a repository requires a separate route and exact PM approval.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.4.
