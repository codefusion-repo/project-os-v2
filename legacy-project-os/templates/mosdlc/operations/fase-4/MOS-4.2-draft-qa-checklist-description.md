# MOS-4.2 draft-qa-checklist-description

MOSDLC:
  ID: MOS-4.2
  Phase: Fase 4 - Testing / QA
  Surface: actor.browser_chat
  Compatibility source: templates/operations/18-draft-human-qa-checklist.md
  Classification: variant; merge-candidate (con MOS-4.1 vía fuente del checklist)
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state

OPERATION:
  Draft a human QA checklist from a stable feature description without executing QA.
  Source map summary: Draftea el checklist humano de QA desde una descripción o feature. Validar features descritas sin issue/PR ancla. Convierte la descripción en pasos verificables por un humano.

INPUT:
  DESCRIPTION=<DESCRIPTION>
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
  Read DESCRIPTION, repository context when needed, and any stable acceptance basis live.
  Treat the QA recipient as outside the kernel actor set; the template drafts checklist text only.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Convert DESCRIPTION into human-verifiable QA steps, expected observations, and ambiguity notes.
  Flag missing acceptance criteria as status.needs_pm_decision instead of inventing them.
  Return status.needs_context when the feature context cannot be inspected enough to draft a meaningful checklist.
  Do not create an issue, execute QA, mutate GitHub, or claim that the described feature passed.

OUTPUT:
  output.status_result carrying the drafted human QA checklist or the fail-closed status.

LIMITS:
  Draft-only/read-only checklist drafting; no QA execution, no repository or GitHub mutation, and no claim that human QA was completed.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-4.5.
