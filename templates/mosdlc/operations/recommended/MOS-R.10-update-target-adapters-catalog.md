# MOS-R.10 update-target-adapters-catalog

MOSDLC:
  ID: MOS-R.10
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat to actor.terminal_agent
  Compatibility source: templates/operations/23-upgrade-kernel-adoption-in-target.md
  Classification: accepted-recommended; alias (de MOS-0.4)
  Workflow: workflow.target_adoption
  Mode: mode.delegated_commit_pr
  Output: output.adoption_packet, output.route_prompt
  Evidence: evidence.target_adoption, evidence.branch_preflight, evidence.pm_approval, evidence.validation_output

OPERATION:
  Update a target project's adapters to a new catalog/kernel version through a delegated, exactly approved write route.
  Source map summary: Actualiza adapters de targets a una nueva versión de catálogo/kernel. Propagar upgrades de catálogo sin drift masivo. Igual que MOS-0.4; crítico durante la migración MOSDLC.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.target_adoption with mode.delegated_commit_pr and emit only the declared output contracts.
  Apply boundary.branch_preflight, boundary.no_main_edits, boundary.separate_pm_approval, boundary.validation_discipline, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/23-upgrade-kernel-adoption-in-target.md as compatibility source for this recommended operation shape; MOS-R.10 is an alias of MOS-0.4 for catalog/kernel version propagation.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read the target repository's current adapters, adopted kernel version, and the new catalog/kernel version evidence live at execution time.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft the adoption update packet for the target; the terminal-agent write requires separate exact PM approval for writing in that target, branch preflight, proportional validation, and a draft PR.
  Fail closed to status.needs_context when the target's adapters, adoption evidence, or the new catalog/kernel version cannot be read.
  Do not merge, close, tag, release, change settings, or edit the target's default branch directly.

OUTPUT:
  output.adoption_packet plus output.route_prompt for the delegated write, or a fail-closed status when evidence is insufficient.

LIMITS:
  The write route runs only with separate exact PM approval for that target; merge and closure stay with the Human PM.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-0.5 per updated target.
