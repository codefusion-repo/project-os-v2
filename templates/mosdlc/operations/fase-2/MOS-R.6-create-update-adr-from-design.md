# MOS-R.6 create-update-adr-from-design

MOSDLC:
  ID: MOS-R.6
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat to actor.terminal_agent
  Compatibility source: templates/operations/22-record-adr-decision.md
  Classification: accepted-recommended; variant (fuente docs, no decisión suelta)
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.route_prompt
  Evidence: evidence.source_basis

OPERATION:
  Create or update ADRs from design or requirements documentation, drafting the delegated write route per decision.
  Source map summary: Crea o actualiza ADRs desde documentación de diseño o requisitos. Llevar a ADR las decisiones que sobreviven a issues. Extrae decisiones estables de docs y draftea ADRs delegados.

INPUT:
  SOURCE_DOCS=<SOURCE_DOCS>
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
  Read SOURCE_DOCS live from the target repository and extract only decisions that are stable and evidence-backed; read existing ADRs to avoid duplicates or contradictions.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Extract stable, issue-surviving decisions from SOURCE_DOCS and draft one ADR (new or update) per decision, following the target repository's ADR conventions when present.
  Draft output.route_prompt for the delegated terminal-agent writes; every file write requires separate exact PM approval, branch preflight, and proportional validation.
  Return status.needs_context when SOURCE_DOCS cannot be read or contains no stable decisions, and status.needs_pm_decision when a candidate decision is ambiguous or conflicts with an existing ADR.
  Do not write files, commit, push, create PRs, or treat drafted routes as approval.

OUTPUT:
  output.route_prompt with the drafted ADR contents and scoped delegated write routes, or a fail-closed status when evidence is insufficient.

LIMITS:
  Draft only; ADR file writes are separate delegated operations with their own gates.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-R.1 per extracted decision.
