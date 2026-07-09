# MOS-4.5 process-qa-checklist-feature

MOSDLC:
  ID: MOS-4.5
  Phase: Fase 4 - Testing / QA
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/30-process-human-qa-results.md
  Classification: variant; merge-candidate (con MOS-4.4 vía fuente del checklist)
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.status_result, output.route_prompt, output.pm_command_bundle
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Classify human QA checklist results for a described feature into issue creation, correction, follow-up, no-op, implementation, or PM decision paths.
  Source map summary: Procesa el resultado del checklist humano de descripción/feature. Cerrar el loop de QA de features sin issue ancla. Clasifica hallazgos hacia issue nuevo, corrección o no-op.

INPUT:
  QA_RESULT=<QA_RESULT>
  DESCRIPTION=<DESCRIPTION>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/30-process-human-qa-results.md as compatibility source for this Fase 4 operation shape.
  Do not delete, rename, renumber, or bypass the 30 compatibility template.

LIVE_STATE:
  Read QA_RESULT, DESCRIPTION when provided, repository context, related docs, and PM decisions live.
  Classify feature QA without assuming an issue or PR anchor exists.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Classify QA_RESULT findings as blocking correction, non-blocking follow-up, new issue, no-op, implementation, or PM decision only when evidence supports that route.
  Draft output.route_prompt only when there is a clear correction target and state that correction routes are non-authorizing outputs.
  Draft output.pm_command_bundle only when a new issue or follow-up is PM-executed and copy-safe.
  Return status.needs_pm_decision when DESCRIPTION, target feature, or route is ambiguous.
  Do not execute QA, edit files, create issues, comment on GitHub, close issues, merge PRs, or authorize corrections.

OUTPUT:
  output.status_result plus output.route_prompt or output.pm_command_bundle only when QA classification selects that draft path.

LIMITS:
  Draft-only classification; route prompts are non-authorizing outputs and issue/follow-up command bundles are PM-executed only.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.8 if new work must become an issue; MOS-4.7 for non-blocking follow-up.
