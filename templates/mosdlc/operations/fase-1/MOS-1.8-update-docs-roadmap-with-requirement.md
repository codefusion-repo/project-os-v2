# MOS-1.8 update-docs-roadmap-with-requirement

MOSDLC:
  ID: MOS-1.8
  Phase: Fase 1 - Requirements, planning, and feasibility
  Surface: actor.browser_chat to actor.terminal_agent
  Compatibility source: templates/operations/27-draft-roadmap-from-docs.md, templates/operations/28-draft-docs-from-description.md
  Classification: variant; merge-candidate (con MOS-1.4 y MOS-1.6)
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.route_prompt, output.pm_command_bundle
  Evidence: evidence.source_basis, evidence.repo_state

OPERATION:
  Draft documentation and roadmap updates for an accepted new requirement while keeping writes behind exact approval gates.

INPUT:
  DESCRIPTION=<DESCRIPTION>
  ROADMAP_ISSUE=<ROADMAP_ISSUE>   # optional
  DOC_TARGET=<DOC_TARGET>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Browser chat drafts with workflow.pm_intake and mode.review_only; terminal writes require a separate route prompt and exact PM approval.
  Apply boundary.draft_only_browser, boundary.copy_safe_commands, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/27-draft-roadmap-from-docs.md and templates/operations/28-draft-docs-from-description.md as compatibility references for roadmap and docs drafting.
  Do not delete, rename, renumber, or bypass the 27 or 28 compatibility templates.

LIVE_STATE:
  Read the accepted requirement description, source docs, roadmap issue when named, repository evidence, and PM decisions live.
  Treat generated docs and command bundles as drafts until the PM approves the exact write action.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft the documentation update needed for the accepted requirement and identify DOC_TARGET when evidence supports it.
  Draft the roadmap update or PM command bundle only when ROADMAP_ISSUE or exact roadmap target is known.
  Route file writes to a terminal agent only through output.route_prompt with exact PM approval, branch preflight, validation, and review.

OUTPUT:
  output.route_prompt for approved file writes plus output.pm_command_bundle for PM-executed roadmap writes, or output.status_result when context is missing.

LIMITS:
  Browser chat drafts only; terminal and GitHub writes require exact PM approval or Human PM execution as applicable.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.1 after the PM applies accepted documentation or roadmap updates.
