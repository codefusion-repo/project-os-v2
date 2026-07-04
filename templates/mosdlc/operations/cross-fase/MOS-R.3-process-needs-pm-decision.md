# MOS-R.3 process-needs-pm-decision

MOSDLC:
  ID: MOS-R.3
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: templates/operations/36-process-needs-pm-decision.md
  Classification: accepted-recommended; replacement
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.status_result, output.route_prompt, output.pm_command_bundle, output.draft_issue
  Evidence: evidence.source_basis, evidence.repo_state

OPERATION:
  Process a status.needs_pm_decision result from any operation into exactly one safe decision outcome, without auto-approving, executing routes, or crossing the source operation's boundary.
  Source map summary: Procesa un status.needs_pm_decision desde su operación de origen con variables target-agnostic claras. Resolver decisiones PM pendientes sin prompts ad hoc. Clasifica hacia una salida segura.

INPUT:
  DECISION_SOURCE=<DECISION_SOURCE>
  DECISION_CONTEXT=<DECISION_CONTEXT>
  DECISION_QUESTION=<DECISION_QUESTION>
  DECISION_OPTIONS=<DECISION_OPTIONS>
  OPTIONS_IMPACT=<OPTIONS_IMPACT>   # optional
  PM_DECISION=<PM_DECISION>   # optional
  PM_CLARIFICATION=<PM_CLARIFICATION>   # optional
  ISSUE_NUMBER=<ISSUE_NUMBER>   # optional
  PR_NUMBER=<PR_NUMBER>   # optional
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  ROADMAP_ISSUE=<ROADMAP_ISSUE>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

  Variable meaning, target-agnostic for any project type:
  - DECISION_SOURCE: the operation, template, report, or status source that returned status.needs_pm_decision.
  - DECISION_CONTEXT: what was happening when the decision became necessary.
  - DECISION_QUESTION: the single question the PM must answer.
  - DECISION_OPTIONS: the available options as the source operation stated them.
  - OPTIONS_IMPACT: tradeoffs or impact per option, when known.
  - PM_DECISION: the explicit PM decision when the PM already chose; it never authorizes writes by itself.
  - PM_CLARIFICATION: a PM clarification that narrows the question without deciding it.
  - ISSUE_NUMBER, PR_NUMBER, TARGET_REPOSITORY, ROADMAP_ISSUE: live target references when relevant.

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/36-process-needs-pm-decision.md as compatibility source; its variables map as ORIGINATING_OPERATION to DECISION_SOURCE, STATUS_CONTEXT to DECISION_CONTEXT, and OPTIONS_TRADEOFFS to DECISION_OPTIONS plus OPTIONS_IMPACT.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read DECISION_SOURCE as the operation, template, or report that produced status.needs_pm_decision; when it can be identified in the catalog or docs, compare the requested decision against that operation's workflow, output, limits, and recommended next operation.
  Read ISSUE_NUMBER, PR_NUMBER, TARGET_REPOSITORY, and ROADMAP_ISSUE live when provided; treat DECISION_CONTEXT, DECISION_OPTIONS, and OPTIONS_IMPACT as claims or evidence leads, not proof.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Classify the pending PM decision into exactly one safe decision category:
  - missing-context: required context or live evidence is missing; return status.needs_context naming exactly what is missing.
  - choose-route: the PM must choose one route among DECISION_OPTIONS; present the options and their impact and return status.needs_pm_decision until PM_DECISION or PM_FEEDBACK_HUMANO makes the choice explicit.
  - approve-correction: the PM approves a scoped correction route; draft output.route_prompt toward MOS-3.5 as a non-authorizing output.
  - create-follow-up: non-blocking work should be tracked separately; draft output.draft_issue content or an output.pm_command_bundle toward MOS-3.3 for Human PM-executed creation.
  - stop-no-op: the PM chooses not to proceed; record the stop decision and end the route.
  - return-to-source: the recorded PM decision is sufficient; return the decision to DECISION_SOURCE so that operation continues under its own gates.
  - need-more-evidence: more evidence is required before any route can be chosen; name the exact evidence and return status.needs_context.
  Prefer return-to-source when the source operation can safely continue.
  Use PM_DECISION or PM_FEEDBACK_HUMANO only for the point explicitly decided; never infer approval from silence, partial answers, or context.
  Use PM_CLARIFICATION or PM_QUESTION_HUMANO to narrow DECISION_QUESTION without replacing required evidence.
  If the evidence contains secrets, credentials, tokens, or secret-looking values, return status.blocked and request a redacted source basis.
  Do not execute the selected route, mutate files or GitHub state, or treat any decision as write permission; a future write operation must independently receive exact PM approval and satisfy its own gates.

OUTPUT:
  output.status_result with: decision source and context; the decision question, options, and impact considered; the selected decision category; the live evidence reviewed; any PM decision or evidence still required; and the explicit statement that no approval or lifecycle transition was executed.
  Draft output.route_prompt only for approve-correction; draft output.draft_issue or output.pm_command_bundle only for create-follow-up.

LIMITS:
  Draft-only classification; decision processing only, with no mutation, no hidden workflow engine, no auto-approval, and no automated lifecycle transition.
  Route prompts are non-authorizing outputs and follow-up command bundles are Human PM-executed only.
  Does not replace the source operation's evidence checks and does not process terminal-agent execution reports for normal PR review; MOS-3.7 remains that path when a PR exists.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  Return to DECISION_SOURCE when the PM decision is sufficient; MOS-3.5 for scoped corrections; MOS-3.3 for follow-ups; MOS-R.2 when only routing is still needed; otherwise stop with status.needs_context or status.needs_pm_decision.
