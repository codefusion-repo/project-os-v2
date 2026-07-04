# MOS-R.2 recommend-next-operation

MOSDLC:
  ID: MOS-R.2
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat
  Compatibility source: templates/operations/35-recommend-next-lifecycle-operation.md
  Classification: accepted-recommended; replacement
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state

OPERATION:
  Recommend the next MOSDLC operation from live traceability, recommendation-only.
  Source map summary: Recomienda la siguiente operación MOSDLC desde trazabilidad viva. Routing de ciclo de vida sin razonamiento ad hoc. Read-only y recommendation-only; nunca ejecuta el paso.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional
  PR_NUMBER=<PR_NUMBER>   # optional
  ROADMAP_ISSUE=<ROADMAP_ISSUE>   # optional
  CURRENT_STATUS=<CURRENT_STATUS>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/35-recommend-next-lifecycle-operation.md as compatibility source for this recommended operation shape.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read issue, PR, roadmap, and repository state live from GitHub and git at execution time; treat CURRENT_STATUS as a claim until live evidence confirms it.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Read-only analysis of live traceability to recommend exactly one next MOSDLC operation, with the evidence that supports it and safe alternatives when the evidence is ambiguous.
  Return status.needs_context when live traceability cannot be read or is insufficient to recommend safely.
  Do not execute, draft, or authorize the recommended operation; the Human PM invokes it.

OUTPUT:
  output.status_result with the recommended next operation, the live evidence reviewed, and safe alternatives when relevant.

LIMITS:
  Read-only and recommendation-only; the Human PM decides and invokes the recommended operation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  The recommended operation itself, invoked by the Human PM.
