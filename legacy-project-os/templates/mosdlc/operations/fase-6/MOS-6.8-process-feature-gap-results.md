# MOS-6.8 process-feature-gap-results

MOSDLC:
  ID: MOS-6.8
  Phase: Fase 6 - Maintenance and tooling
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: none
  Classification: new
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.status_result, output.route_prompt, output.pm_command_bundle
  Evidence: evidence.source_basis, evidence.repo_state

OPERATION:
  Process system functional-gap results for production readiness.
  Source map summary: Procesa los resultados de gaps funcionales del sistema para production readiness. Priorizar el cierre de gaps funcionales. Clasifica gaps hacia issues nuevos o follow-ups.

INPUT:
  AUDIT_RESULT=<AUDIT_RESULT>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  This is a new MOSDLC operation with no direct 00-37 compatibility source.
  Do not delete, rename, renumber, or bypass any 00-37 compatibility template.

LIVE_STATE:
  Read AUDIT_RESULT from MOS-6.2 and related requirements or roadmap evidence live.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Classify AUDIT_RESULT gaps as new implementation work, non-blocking follow-up, or PM decision only when evidence supports that route.
  Draft output.pm_command_bundle for new bounded issue creation that the Human PM may execute.
  Return status.needs_context when AUDIT_RESULT or its evidence basis cannot be inspected.
  Do not create issues, edit files, comment on GitHub, or implement missing functionality.

OUTPUT:
  output.status_result plus output.route_prompt or output.pm_command_bundle only when the classification selects that draft path.

LIMITS:
  Draft-only classification; route prompts are non-authorizing outputs and command bundles are Human PM-executed only.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.8 for new implementation work; MOS-3.3 for non-blocking follow-up.
