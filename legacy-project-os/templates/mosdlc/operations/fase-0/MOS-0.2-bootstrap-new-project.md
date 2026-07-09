# MOS-0.2 bootstrap-new-project

MOSDLC:
  ID: MOS-0.2
  Phase: Fase 0 - Adaptation
  Surface: actor.browser_chat
  Compatibility source: templates/operations/02-bootstrap-new-project.md
  Classification: replacement
  Workflow: workflow.target_adoption
  Mode: mode.review_only
  Output: output.adoption_packet
  Evidence: evidence.target_adoption

OPERATION:
  Draft the initial Project OS adoption package for a new target repository.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  DESCRIPTION=<DESCRIPTION>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.target_adoption with mode.review_only.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/02-bootstrap-new-project.md as the replacement source until MOSDLC migration is complete.
  Do not delete, rename, renumber, or bypass the 02 compatibility template.

LIVE_STATE:
  Read TARGET_REPOSITORY adoption evidence live when available.
  Confirm whether adoption files already exist before drafting new adapter content.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft an adoption packet with adapter drafts, a foundational roadmap draft, and a PM checklist.
  Preserve target-owned product truth, notes, security/domain constraints, and validation expectations.
  If the PM wants files written, stop at a route prompt for a terminal agent; this operation remains draft-only.

OUTPUT:
  output.adoption_packet with target identity, current adoption state, adapter drafts, checklist, rollback note, and safe next operation.

LIMITS:
  No file, git, GitHub, settings, release, label, merge, closure, product-code, runtime-config, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-0.5 verify-target-adoption.
