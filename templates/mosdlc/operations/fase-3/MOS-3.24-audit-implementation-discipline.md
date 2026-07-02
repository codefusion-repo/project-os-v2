# MOS-3.24 audit-implementation-discipline

MOSDLC:
  ID: MOS-3.24
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat / actor.terminal_agent
  Compatibility source: templates/operations/25-audit-implementation-discipline-gaps.md
  Classification: replacement
  Workflow: workflow.implementation_discipline_audit
  Mode: mode.review_only
  Output: output.draft_issue, output.review_result
  Evidence: evidence.repo_state

OPERATION:
  Audit implementation-discipline gaps read-only against repository evidence.
  Source map summary: Audita gaps de disciplina de implementación contra boundary.implementation_discipline. Detectar deuda de disciplina con evidencia de archivos y líneas. Auditoría read-only con findings y drafts de follow-up.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PATH_SCOPE=<PATH_SCOPE>   # optional
  FOCUS=<FOCUS>   # optional
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional
  PR_NUMBER=<PR_NUMBER>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.implementation_discipline_audit with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/25-audit-implementation-discipline-gaps.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 25 compatibility template.

LIVE_STATE:
  Read repository files, optional issue or PR scope, path scope, focus, and PM decisions live.
  Inspect implementation evidence directly and keep findings evidence-backed by file and line where possible.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Inspect selected repository evidence against boundary.implementation_discipline, boundary.primary_path_discipline, and boundary.validation_discipline.
  Report only evidence-backed findings with file/line anchors where possible and recommend correction or follow-up.
  Do not refactor, edit files, mutate GitHub, or turn the audit into style-only commentary.

OUTPUT:
  output.review_result with implementation-discipline findings, or output.draft_issue/status_result when appropriate.

LIMITS:
  Draft-only or read-only operation; no file, git, GitHub, settings, release, tag, label, merge, closure, runtime-config, secret-store, product-code, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.26.
