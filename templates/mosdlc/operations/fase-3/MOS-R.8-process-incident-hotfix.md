# MOS-R.8 process-incident-hotfix

MOSDLC:
  ID: MOS-R.8
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: none
  Classification: accepted-recommended; new
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.status_result, output.draft_issue, output.route_prompt, output.pm_command_bundle
  Evidence: evidence.source_basis, evidence.repo_state

OPERATION:
  Process an incident or critical bug: intake, triage, hotfix issue drafting, and postmortem follow-up, draft-only.
  Source map summary: Procesa un incidente o bug crítico: intake, triage, hotfix issue y postmortem. Dar ruta explícita a incidentes sin improvisar. Clasifica severidad y draftea hotfix issue, ruta y follow-up postmortem.

INPUT:
  INCIDENT_DESCRIPTION=<INCIDENT_DESCRIPTION>
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  PR_NUMBER=<PR_NUMBER>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  No 00-37 compatibility source is mapped for this recommended operation.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read INCIDENT_DESCRIPTION as a claim and verify impact against live repository, issue, and PR evidence when available.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Triage the incident: classify severity and user impact only when evidence supports that route, and separate the blocking hotfix from non-blocking postmortem work.
  Draft the hotfix issue (output.draft_issue) and, when a scoped agent fix is viable, an output.route_prompt toward MOS-3.4 as a non-authorizing output.
  Draft an output.pm_command_bundle for Human PM-executed issue creation, and a postmortem follow-up draft toward MOS-3.3.
  Return status.needs_context when the incident cannot be confirmed from evidence, and status.needs_pm_decision when severity or route requires an explicit PM choice.
  Redact any credentials or secret-looking values in incident evidence as [REDACTED].
  Do not execute fixes, edit files, create issues, comment on GitHub, roll back, or authorize deployment.

OUTPUT:
  output.status_result with the triage classification, plus output.draft_issue, output.route_prompt, or output.pm_command_bundle only when the classification selects that draft path.

LIMITS:
  Draft-only classification; route prompts are non-authorizing outputs and command bundles are Human PM-executed only.
  Does not decide severity policy for the PM and does not bypass normal review; the PM decision governs the hotfix route.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.4 for the hotfix; MOS-3.3 for the postmortem follow-up.
