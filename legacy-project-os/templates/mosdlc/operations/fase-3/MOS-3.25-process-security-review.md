# MOS-3.25 process-security-review

MOSDLC:
  ID: MOS-3.25
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/31-process-security-review-results.md
  Classification: replacement
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.pm_command_bundle, output.route_prompt, output.status_result
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Process security review results into correction, follow-up, or review-before-close routing.
  Source map summary: Procesa el resultado de una revisión de seguridad y clasifica la ruta segura. Convertir findings de seguridad en corrección o follow-up. Clasifica bloqueantes y no bloqueantes sin ejecutar nada.

INPUT:
  SECURITY_REVIEW_RESULT=<SECURITY_REVIEW_RESULT>
  PR_NUMBER=<PR_NUMBER>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/31-process-security-review-results.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 31 compatibility template.

LIVE_STATE:
  Read SECURITY_REVIEW_RESULT, related PR or issue, security evidence, and PM decisions live.
  Redact secret-looking values as [REDACTED] and never request hidden environment values.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Classify SECURITY_REVIEW_RESULT findings into blocking correction, non-blocking follow-up, no-op, or PM decision.
  Draft output.route_prompt for blocking security corrections or output.pm_command_bundle for non-blocking follow-up issue creation.
  Never expose, request, summarize, quote, or store secret values; redact secret-looking content as [REDACTED].
  Apply strict secret redaction; report only paths, variable names, risk types, and [REDACTED] placeholders when sensitive values appear.

OUTPUT:
  output.status_result plus output.route_prompt or output.pm_command_bundle only when review classification selects that draft path.

LIMITS:
  Security result processing only; no scanner execution, no secret exposure, and no repository or GitHub mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.5.
