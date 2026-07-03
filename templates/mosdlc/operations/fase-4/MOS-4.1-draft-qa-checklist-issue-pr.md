# MOS-4.1 draft-qa-checklist-issue-pr

MOSDLC:
  ID: MOS-4.1
  Phase: Fase 4 - Testing / QA
  Surface: actor.browser_chat
  Compatibility source: templates/operations/18-draft-human-qa-checklist.md
  Classification: replacement
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state

OPERATION:
  Draft a human QA checklist for an issue or PR without executing QA.
  Source map summary: Draftea el checklist humano de QA enfocado en un issue/PR. Cubrir lo no automatizable con QA humano dirigido. Extrae criterios del issue/PR a pasos verificables por un humano.

INPUT:
  ISSUE_NUMBER=<ISSUE_NUMBER>
  PR_NUMBER=<PR_NUMBER>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/18-draft-human-qa-checklist.md as compatibility source for this Fase 4 operation shape.
  Do not delete, rename, renumber, or bypass the 18 compatibility template.

LIVE_STATE:
  Read the issue, PR when provided, requirements, acceptance basis, and observable changed behavior live.
  Treat the QA recipient as outside the kernel actor set; the template drafts checklist text only.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Extract human-verifiable flows, edge cases, accessibility or UX checks, and acceptance criteria from live evidence.
  Draft a copy-ready checklist for the Human PM or QA recipient.
  Return status.needs_context when issue, PR, requirements, or acceptance evidence cannot be inspected.
  Do not execute product QA, mark QA complete, mutate GitHub, or move the issue toward closure.

OUTPUT:
  output.status_result carrying the drafted human QA checklist or the fail-closed status.

LIMITS:
  Draft-only/read-only checklist drafting; no QA execution, no repository or GitHub mutation, and no claim that human QA was completed.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-4.4.
