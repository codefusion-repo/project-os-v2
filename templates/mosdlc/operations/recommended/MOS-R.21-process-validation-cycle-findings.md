# MOS-R.21 process-validation-cycle-findings

MOSDLC:
  ID: MOS-R.21
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: none
  Classification: accepted-recommended; new
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.status_result, output.route_prompt, output.pm_command_bundle
  Evidence: evidence.source_basis, evidence.repo_state

OPERATION:
  Process the findings of a validation cycle into bounded, traceable follow-ups, draft-only.
  Source map summary: Procesa hallazgos de un ciclo de validación y los convierte en follow-ups acotados. Capturar fricción real del target como trabajo trazable. Clasifica hallazgos y draftea follow-ups para el Humano PM.

INPUT:
  VALIDATION_FINDINGS=<VALIDATION_FINDINGS>
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  VALIDATION_CYCLE_TYPE=<VALIDATION_CYCLE_TYPE>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

  VALIDATION_FINDINGS carries the cycle's findings from any validation surface: internal QA, staging validation, beta rollout, UAT, TestFlight/internal testing, release candidate validation, playtest, balance test, content QA, performance validation, integration test, consumer validation, release candidate trial, pilot rollout, acceptance test, or operational validation.

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  No 00-37 compatibility source is mapped for this recommended operation.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read VALIDATION_FINDINGS as claims or evidence leads and verify against live repository evidence when possible.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Classify each finding as blocking correction, non-blocking follow-up, product/roadmap feedback, or PM decision only when evidence supports that route.
  Draft output.route_prompt only for blocking corrections as a non-authorizing output, and output.pm_command_bundle only for Human PM-executed follow-up issue creation.
  Return status.needs_context when VALIDATION_FINDINGS or its evidence basis cannot be inspected, and status.needs_pm_decision when a finding changes scope or product direction.
  Do not create issues, execute corrections, edit files, or close the validation cycle.

OUTPUT:
  output.status_result with the per-finding classification, plus output.route_prompt or output.pm_command_bundle only when the classification selects that draft path.

LIMITS:
  Draft-only classification; route prompts are non-authorizing outputs and follow-up command bundles are Human PM-executed only.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.3 per finding.
