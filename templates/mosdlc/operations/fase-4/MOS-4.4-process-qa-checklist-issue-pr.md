# MOS-4.4 process-qa-checklist-issue-pr

MOSDLC:
  ID: MOS-4.4
  Phase: Fase 4 - Testing / QA
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/30-process-human-qa-results.md
  Classification: replacement
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.status_result, output.route_prompt, output.pm_command_bundle
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Classify human QA checklist results for an issue or PR into correction, follow-up, no-op, review-before-close, implementation, or PM decision paths.
  Source map summary: Procesa el resultado del checklist humano de issue/PR. Convertir QA humano en corrección, follow-up o avance. Clasifica bloqueantes y no bloqueantes sin ejecutar nada.

INPUT:
  QA_RESULT=<QA_RESULT>
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional
  PR_NUMBER=<PR_NUMBER>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/30-process-human-qa-results.md as compatibility source for this Fase 4 operation shape.
  Do not delete, rename, renumber, or bypass the 30 compatibility template.

LIVE_STATE:
  Read QA_RESULT, related issue or PR, acceptance criteria, checklist source, and PM decisions live.
  If ISSUE_NUMBER and PR_NUMBER are both omitted, derive exactly one target from QA_RESULT and live traceability or fail closed.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Classify QA_RESULT findings as blocking correction, non-blocking follow-up, no-op, review-before-close, implementation, or PM decision only when evidence supports that route.
  Draft output.route_prompt only for blocking QA corrections and state that correction routes are non-authorizing outputs.
  Draft output.pm_command_bundle only for non-blocking follow-ups that the Human PM may execute.
  Route passing QA toward review-before-close only when issue or PR evidence supports it; otherwise return status.needs_context or status.needs_pm_decision.
  Do not execute QA, edit files, create issues, comment on GitHub, close issues, merge PRs, or authorize corrections.

OUTPUT:
  output.status_result plus output.route_prompt or output.pm_command_bundle only when QA classification selects that draft path.

LIMITS:
  Draft-only classification; route prompts are non-authorizing outputs and follow-up command bundles are PM-executed only.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-4.8 for blocking QA findings; MOS-4.7 for non-blocking follow-up; MOS-3.7 when QA evidence supports review-before-close.
