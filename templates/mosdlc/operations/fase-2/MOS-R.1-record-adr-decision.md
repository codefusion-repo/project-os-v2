# MOS-R.1 record-adr-decision

MOSDLC:
  ID: MOS-R.1
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat to actor.terminal_agent
  Compatibility source: templates/operations/22-record-adr-decision.md
  Classification: accepted-recommended; replacement
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.route_prompt
  Evidence: evidence.source_basis

OPERATION:
  Draft an ADR that records a stable PM decision plus the delegated write route for a terminal agent.
  Source map summary: Registra una decisión PM como ADR draftado y ruta de escritura delegada. Preservar decisiones que sobreviven a los issues. Draftea el ADR; la escritura del archivo exige aprobación exacta.

INPUT:
  DECISION=<DECISION>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/22-record-adr-decision.md as compatibility source for this recommended operation shape.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read DECISION as the PM decision to preserve; read the target repository's existing decisions directory and ADR conventions live when they exist.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft the ADR content (context, decision, consequences) from DECISION and its evidence basis, following the target repository's ADR conventions when present.
  Draft output.route_prompt for the delegated terminal-agent file write; the write itself requires separate exact PM approval, branch preflight, and proportional validation.
  Return status.needs_context when DECISION is missing, ambiguous, or its evidence basis cannot be inspected.
  Do not write files, commit, push, create PRs, or treat the drafted route as approval.

OUTPUT:
  output.route_prompt with the drafted ADR content and the scoped delegated write route, or a fail-closed status when evidence is insufficient.

LIMITS:
  Draft only; the ADR file write is a separate delegated operation with its own gates.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.1 once the decision is recorded.
