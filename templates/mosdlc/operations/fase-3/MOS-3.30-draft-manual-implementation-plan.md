# MOS-3.30 draft-manual-implementation-plan

MOSDLC:
  ID: MOS-3.30
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/33-draft-manual-implementation-plan.md
  Classification: replacement
  Workflow: workflow.issue_implementation_manual
  Mode: mode.review_only
  Output: output.manual_implementation_plan
  Evidence: evidence.issue_scope, evidence.repo_state, evidence.source_basis

OPERATION:
  Draft a human-executable implementation plan for one scoped issue without editing files.
  Source map summary: Draftea el paso a paso humano-ejecutable para implementar un issue sin escribir archivos. Implementar cuando no hay terminal agent disponible o apropiado. Plan detallado por archivo y anclas; nunca afirma haber editado código.

INPUT:
  ISSUE_NUMBER=<ISSUE_NUMBER>
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  PATH_SCOPE=<PATH_SCOPE>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.issue_implementation_manual with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/33-draft-manual-implementation-plan.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 33 compatibility template.

LIVE_STATE:
  Read issue objective, scope, out-of-scope, acceptance criteria, source basis, repository files, and validation expectations live.
  Treat the plan as human-executable instructions; browser chat did not edit code, run validation, or mutate git/GitHub.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft output.manual_implementation_plan with objective, files to inspect, files to modify, anchored change plan, reasoning, validation commands, manual QA, risks, rollback, and next operation.
  State explicitly that no code was edited, no files were written, and no git or GitHub mutation occurred.
  Return status.needs_context when issue scope, repository context, validation expectations, or implementation anchors are insufficient.
  Preserve manual implementation behavior as browser-chat and Human PM draft-only; never imply browser chat edited code.

OUTPUT:
  output.manual_implementation_plan, or output.status_result when issue scope or repository anchors are insufficient.

LIMITS:
  Manual implementation planning only; browser chat never edits files, runs validation, commits, pushes, opens PRs, or claims implementation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.31.
