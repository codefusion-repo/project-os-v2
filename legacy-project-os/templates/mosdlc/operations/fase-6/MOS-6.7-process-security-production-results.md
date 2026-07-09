# MOS-6.7 process-security-production-results

MOSDLC:
  ID: MOS-6.7
  Phase: Fase 6 - Maintenance and tooling
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/31-process-security-review-results.md
  Classification: variant (contexto production readiness)
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.status_result, output.route_prompt, output.pm_command_bundle
  Evidence: evidence.source_basis, evidence.repo_state

OPERATION:
  Process security-for-production-readiness results into blocking or deferrable actions.
  Source map summary: Procesa los resultados de seguridad para production readiness. Convertir riesgos detectados en acciones concretas. Clasifica bloqueantes y diferibles sin ejecutar nada.

INPUT:
  SECURITY_REVIEW_RESULT=<SECURITY_REVIEW_RESULT>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/31-process-security-review-results.md as compatibility source for this Fase 6 operation shape.
  Do not delete, rename, renumber, or bypass the 31 compatibility template.

LIVE_STATE:
  Read SECURITY_REVIEW_RESULT from MOS-6.1 and any related PM decisions live.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Classify SECURITY_REVIEW_RESULT findings as blocking correction, non-blocking follow-up, or PM decision only when evidence supports that route.
  Draft output.route_prompt only for blocking production-security corrections and state that correction routes are non-authorizing outputs.
  Draft output.pm_command_bundle only for non-blocking follow-ups that the Human PM may execute.
  Return status.needs_context when SECURITY_REVIEW_RESULT or its evidence basis cannot be inspected.
  Do not execute corrections, edit files, create issues, comment on GitHub, or authorize deployment.

OUTPUT:
  output.status_result plus output.route_prompt or output.pm_command_bundle only when the classification selects that draft path.

LIMITS:
  Draft-only classification; route prompts are non-authorizing outputs and follow-up command bundles are Human PM-executed only.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.5 for blocking findings; MOS-3.3 for non-blocking follow-up.
