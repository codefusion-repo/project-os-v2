# MOS-0.5 verify-target-adoption

MOSDLC:
  ID: MOS-0.5
  Phase: Fase 0 - Adaptation
  Surface: actor.browser_chat or actor.terminal_agent
  Compatibility source: templates/operations/03-verify-target-adoption.md
  Classification: replacement
  Workflow: workflow.target_adoption
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.target_adoption

OPERATION:
  Audit read-only whether a target repository adoption exists, is correct, and points to the current kernel standard.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.target_adoption with mode.review_only.
  Apply boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/03-verify-target-adoption.md as the replacement source until MOSDLC migration is complete.
  Do not delete, rename, renumber, or bypass the 03 compatibility template.

LIVE_STATE:
  Read target adapters, metadata, roadmap anchors, target notes, and validation guidance live.
  Compare target adoption evidence against canonical adapter expectations and MOSDLC compatibility sources.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Report present, missing, stale, drifted, or unsafe adoption elements.
  Name any missing live evidence precisely and fail closed when target adoption cannot be inspected.
  Recommend update or lifecycle routing without applying fixes.

OUTPUT:
  output.status_result with adoption findings, evidence read, gaps, risk, and safe next operation.

LIMITS:
  Read-only audit; no file, git, GitHub, settings, release, label, merge, closure, product-code, runtime-config, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-0.4 when adoption drift needs update; otherwise stop with the verified adoption result for PM routing.
