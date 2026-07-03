# MOS-4.6 process-production-readiness-checklist

MOSDLC:
  ID: MOS-4.6
  Phase: Fase 4 - Testing / QA
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/30-process-human-qa-results.md
  Classification: variant; merge-candidate (con MOS-4.4 vía alcance readiness)
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.status_result, output.route_prompt, output.pm_command_bundle
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Classify production-readiness checklist results into readiness gaps, follow-up, no-op, implementation, correction, or PM decision paths without executing deployment behavior.
  Source map summary: Procesa el resultado del checklist humano de production readiness. Decidir si el proyecto avanza hacia despliegue. Clasifica gaps de readiness y recomienda la fase segura.

INPUT:
  QA_RESULT=<QA_RESULT>
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
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
  Read QA_RESULT, target repository evidence, readiness checklist source, docs, and PM decisions live.
  Keep production-readiness processing as QA/readiness classification only; do not migrate or implement Fase 5 deployment behavior.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Classify QA_RESULT gaps as blocking readiness correction, non-blocking follow-up, no-op, implementation, security review, or PM decision only when evidence supports that route.
  Draft output.route_prompt only for scoped correction or implementation routing and state that route prompts are non-authorizing outputs.
  Draft output.pm_command_bundle only for Human PM-executed follow-ups.
  Recommend MOS-R.4 for phase readiness review before any later deployment-phase operation.
  Do not execute QA, draft deploy commands, execute deployment, add deployment workflow ids, mutate GitHub, or claim production readiness is complete.

OUTPUT:
  output.status_result plus output.route_prompt or output.pm_command_bundle only when readiness classification selects that draft path.

LIMITS:
  Draft-only/read-only readiness classification; no deployment behavior, no repository or GitHub mutation, and no authorization to proceed to production.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-R.4 before any later phase transition.
