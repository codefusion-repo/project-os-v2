# MOS-3.6 draft-closeout-commands

MOSDLC:
  ID: MOS-3.6
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/10-draft-pr-closeout-and-cleanup-command.md
  Classification: replacement
  Workflow: workflow.review_before_close
  Mode: mode.review_only
  Output: output.pm_command_bundle
  Evidence: evidence.issue_scope, evidence.pr_diff, evidence.validation_output

OPERATION:
  Draft copy-safe PR and issue closeout commands for the Human PM after review-before-close has resolved.
  Source map summary: Draftea el paquete de cierre y limpieza de issue/PR según estado vivo. Cerrar con evidencia completa y sin escritura del agente. Bundle copy-safe que ejecuta el Humano PM.

INPUT:
  PR_NUMBER=<PR_NUMBER>
  ISSUE_NUMBER=<ISSUE_NUMBER>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_before_close with mode.review_only and emit only the declared output contracts.
  Apply boundary.copy_safe_commands, boundary.review_before_close, boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/10-draft-pr-closeout-and-cleanup-command.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 10 compatibility template.

LIVE_STATE:
  Read the linked issue, PR diff, review result, validation evidence, branch state, and PM decisions live.
  Draft closeout commands only after review-before-close has enough code-backed evidence to support closure.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft copy-safe commands for the Human PM to comment, mark ready when applicable, merge, close, and clean up only when evidence supports it.
  Keep scope, risk, and rollback outside executable blocks and target exact repository, issue, PR, and branch names.
  Do not merge, close, delete branches, label, or mutate GitHub from the template.
  Preserve review-before-close behavior; this template does not merge or close.

OUTPUT:
  output.pm_command_bundle for Human PM closeout only after review-before-close evidence is sufficient.

LIMITS:
  Closeout command drafting only; the template never merges, closes, labels, marks ready, comments, deletes branches, or mutates GitHub.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.9.
