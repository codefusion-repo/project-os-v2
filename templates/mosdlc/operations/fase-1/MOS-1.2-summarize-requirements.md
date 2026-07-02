# MOS-1.2 summarize-requirements

MOSDLC:
  ID: MOS-1.2
  Phase: Fase 1 - Requirements, planning, and feasibility
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: none
  Classification: new
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.source_basis

OPERATION:
  Summarize and structure identified requirements into a PM-verifiable basis before documentation or planning.

INPUT:
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
  Read the interview notes, PM-provided source basis, and cited repository evidence live.
  Treat summaries as PM-verifiable drafts, not as durable proof of current repository or roadmap state.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Group requirements into functional, non-functional, constraints, assumptions, dependencies, and open questions.
  Preserve ambiguity instead of inventing acceptance criteria or priorities.
  Return status.needs_pm_decision when requirements conflict or need PM prioritization.

OUTPUT:
  output.status_result with the structured requirement summary, unresolved questions, and safe next operation.

LIMITS:
  Browser chat drafts only; no file, git, GitHub, settings, release, label, merge, closure, product-code, runtime-config, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-1.3 verify-requirements-feasibility.
