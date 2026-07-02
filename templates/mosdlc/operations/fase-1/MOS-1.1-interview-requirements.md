# MOS-1.1 interview-requirements

MOSDLC:
  ID: MOS-1.1
  Phase: Fase 1 - Requirements, planning, and feasibility
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: none
  Classification: new
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.source_basis

OPERATION:
  Conduct a guided PM interview to elicit functional and non-functional requirements without writing repository files.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  This is a new MOSDLC operation with no direct 00-37 compatibility source.
  Do not delete, rename, renumber, or bypass any 00-37 compatibility template.

LIVE_STATE:
  Read PM-provided context, cited docs, roadmap anchors, and target repository evidence live when needed for the interview.
  Treat interview answers as source basis for drafting, not as authorization to write files.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Ask focused questions that separate functional requirements, non-functional requirements, constraints, assumptions, and open PM decisions.
  Summarize confirmed points and unresolved questions after each useful batch.
  Stop with status.needs_context or status.needs_pm_decision when source basis or PM choices are insufficient.

OUTPUT:
  output.status_result with elicited requirements, open questions, evidence read, and the safe next operation.

LIMITS:
  Browser chat drafts only; no file, git, GitHub, settings, release, label, merge, closure, product-code, runtime-config, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-1.2 summarize-requirements.
