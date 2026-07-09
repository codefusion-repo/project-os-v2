# MOS-3.1 draft-next-issue-from-traceability

MOSDLC:
  ID: MOS-3.1
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/06-draft-create-next-issue-command-from-traceability.md
  Classification: replacement
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.pm_command_bundle
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Infer the next single implementation issue from live traceability and roadmap evidence, then draft a Human PM command bundle.
  Source map summary: Infiere el próximo outcome real desde trazabilidad viva y roadmap y draftea su creación. Crear el siguiente issue único sin perder el hilo del roadmap. Lee estado vivo y draftea el bundle de creación para el Humano PM.

INPUT:
  ROADMAP_ISSUE=<ROADMAP_ISSUE>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.copy_safe_commands, boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/06-draft-create-next-issue-command-from-traceability.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 06 compatibility template.

LIVE_STATE:
  Read roadmap, open issues, merged/closed work, linked PRs, and PM decisions live before choosing the next outcome.
  Treat the command bundle as draft text for the Human PM; GitHub issue creation remains PM-executed.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Identify the single next outcome that is best supported by roadmap and traceability evidence.
  Draft output.pm_command_bundle for the Human PM with one issue body and exact repository target.
  Return status.needs_pm_decision when multiple next outcomes are plausible or source basis conflicts.

OUTPUT:
  output.pm_command_bundle with one Human PM-executed issue creation bundle, or output.status_result when evidence is insufficient.

LIMITS:
  Draft-only or read-only operation; no file, git, GitHub, settings, release, tag, label, merge, closure, runtime-config, secret-store, product-code, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.4.
