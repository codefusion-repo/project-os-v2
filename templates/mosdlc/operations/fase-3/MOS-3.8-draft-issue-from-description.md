# MOS-3.8 draft-issue-from-description

MOSDLC:
  ID: MOS-3.8
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/04-draft-create-issue-command-from-description.md
  Classification: replacement (04 más chequeo de impacto)
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.pm_command_bundle
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Draft a new issue from PM description while checking roadmap and documentation impact.
  Source map summary: Draftea un issue desde una descripción y verifica que no afecte roadmap ni documentación. Capturar trabajo nuevo sin romper la planificación vigente. Convierte la descripción en bundle y chequea impacto contra roadmap y docs.

INPUT:
  DESCRIPTION=<DESCRIPTION>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.copy_safe_commands, boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/04-draft-create-issue-command-from-description.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 04 compatibility template.

LIVE_STATE:
  Read roadmap, requirements/design docs, existing issues, and PM description live before drafting the issue.
  Check whether the description changes roadmap or documentation truth and surface a PM decision when it does.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Turn DESCRIPTION into one scoped issue draft with source basis, scope, out-of-scope, acceptance criteria, validation, risk, and rollback.
  Name any roadmap or documentation impact and route to PM decision when the impact is not a simple implementation issue.
  Draft output.pm_command_bundle only for Human PM execution.

OUTPUT:
  output.pm_command_bundle with a Human PM-executed issue creation bundle, or output.status_result for missing source basis or PM decision.

LIMITS:
  Draft-only or read-only operation; no file, git, GitHub, settings, release, tag, label, merge, closure, runtime-config, secret-store, product-code, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.4.
