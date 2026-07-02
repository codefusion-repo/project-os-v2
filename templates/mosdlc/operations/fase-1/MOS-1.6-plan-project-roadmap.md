# MOS-1.6 plan-project-roadmap

MOSDLC:
  ID: MOS-1.6
  Phase: Fase 1 - Requirements, planning, and feasibility
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/27-draft-roadmap-from-docs.md
  Classification: replacement
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.draft_issue, output.pm_command_bundle
  Evidence: evidence.source_basis, evidence.repo_state

OPERATION:
  Draft the general project roadmap from stable requirements documentation and live repository context.

INPUT:
  SOURCE_DOCS=<SOURCE_DOCS>
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  ROADMAP_ACTION=<ROADMAP_ACTION>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only.
  Apply boundary.draft_only_browser, boundary.copy_safe_commands, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/27-draft-roadmap-from-docs.md as the replacement source for roadmap drafting shape.
  Do not delete, rename, renumber, or bypass the 27 compatibility template.

LIVE_STATE:
  Read SOURCE_DOCS, existing roadmap anchors, linked issues, ADRs, repository state, and PM decisions live.
  Treat roadmap text and command bundles as drafts for the Human PM; GitHub writes remain PM-executed.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Convert stable requirements into a roadmap issue body with phases, outcomes, not-now scope, risks, and validation expectations.
  Draft a copy-safe PM command bundle only when the PM asks for create or update and the exact target is known.
  Return status.needs_pm_decision when priority, scope, or ROADMAP_ACTION is ambiguous.

OUTPUT:
  output.draft_issue for the roadmap body plus output.pm_command_bundle when the PM requests a copy-safe create or update bundle.

LIMITS:
  Browser chat drafts only; the Human PM executes GitHub writes.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.1 or MOS-3.2 depending on the roadmap path selected by the PM.
