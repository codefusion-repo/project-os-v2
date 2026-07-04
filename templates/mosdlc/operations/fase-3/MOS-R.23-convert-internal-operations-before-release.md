# MOS-R.23 convert-internal-operations-before-release

MOSDLC:
  ID: MOS-R.23
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat to actor.terminal_agent
  Compatibility source: none
  Classification: accepted-recommended; new
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.route_prompt, output.draft_issue
  Evidence: evidence.source_basis

OPERATION:
  Draft the removal, hiding, disabling, or conversion of the target's internal-only surfaces before a public release, as a delegated route.
  Source map summary: Remueve, oculta, deshabilita o convierte superficies internal-only del target antes del release público. Publicar sin exponer capacidades internas. Usa el inventario de exposición del catálogo del target y draftea la conversión delegada.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  No 00-37 compatibility source is mapped for this recommended operation.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read the target's internal-only inventory live: its exposure documentation, internal-only operations or surfaces, and the MOS-R.22 review findings; when the target operates this catalog, the map's exposure column is that inventory.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft, per internal-only surface, the decision to remove, hide, disable, or convert it before the public release, with the evidence for each choice.
  Draft output.route_prompt for the delegated terminal-agent conversion changes and output.draft_issue content when the conversion warrants its own scoped issue; the resulting changes require separate exact PM approval.
  Return status.needs_context when the internal-only inventory cannot be read, and status.needs_pm_decision when a surface's disposition requires an explicit PM choice.
  Do not edit files, remove operations, publish, release, or treat drafted routes as approval.

OUTPUT:
  output.route_prompt with the scoped conversion plan per surface plus output.draft_issue content when needed, or a fail-closed status when evidence is insufficient.

LIMITS:
  Draft only; every resulting change requires separate exact PM approval and its own delegated gates.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-R.7 to re-verify publication readiness after conversion.
