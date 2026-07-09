# MOS-3.14 process-traceability-audit

MOSDLC:
  ID: MOS-3.14
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: none
  Classification: new
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.pm_command_bundle, output.route_prompt, output.status_result
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Classify traceability audit findings into correction, follow-up, no-op, or PM decision paths.
  Source map summary: Procesa el resultado de la auditoría de trazabilidad y clasifica la ruta segura. Convertir hallazgos de auditoría en acciones concretas. Clasifica cada hallazgo hacia corrección, follow-up o no-op.

INPUT:
  AUDIT_RESULT=<AUDIT_RESULT>
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional
  PR_NUMBER=<PR_NUMBER>   # optional
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
  Read AUDIT_RESULT, the source audit evidence, related issues/PRs, and PM decisions live.
  Classify findings by blocker, follow-up, no-op, or missing PM decision without mutating GitHub.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Classify AUDIT_RESULT findings into blocking correction, non-blocking follow-up, no-op, or PM decision.
  Draft output.route_prompt for blocking corrections or output.pm_command_bundle for follow-up issue creation when appropriate.
  Do not mutate issues, PRs, comments, labels, branches, or files.

OUTPUT:
  output.status_result plus output.route_prompt or output.pm_command_bundle only when classification selects that draft path.

LIMITS:
  Draft-only or read-only operation; no file, git, GitHub, settings, release, tag, label, merge, closure, runtime-config, secret-store, product-code, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.3.
