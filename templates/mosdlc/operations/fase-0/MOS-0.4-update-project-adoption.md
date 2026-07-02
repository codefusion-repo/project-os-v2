# MOS-0.4 update-project-adoption

MOSDLC:
  ID: MOS-0.4
  Phase: Fase 0 - Adaptation
  Surface: actor.browser_chat to actor.terminal_agent
  Compatibility source: templates/operations/23-upgrade-kernel-adoption-in-target.md
  Classification: replacement
  Workflow: workflow.target_adoption
  Mode: mode.delegated_commit_pr
  Output: output.adoption_packet, output.route_prompt
  Evidence: evidence.target_adoption, evidence.branch_preflight, evidence.pm_approval, evidence.validation_output

OPERATION:
  Refresh an already adopted target repository to the current Project OS adoption standard.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Browser chat drafts with workflow.target_adoption; terminal writes require mode.delegated_commit_pr.
  Apply boundary.branch_preflight, boundary.no_main_edits, boundary.output_not_permission, boundary.no_live_state_durable, boundary.security_privacy, boundary.validation_discipline, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/23-upgrade-kernel-adoption-in-target.md as the replacement source until MOSDLC migration is complete.
  Do not delete, rename, renumber, or bypass the 23 compatibility template.

LIVE_STATE:
  Read current target adapters, kernel adoption metadata, roadmap anchors, and target-owned notes live.
  Detect version drift, stale baseline, missing adapters, roadmap mismatch, and durable live-state risk.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft an adoption-update packet with exact adapter-only changes and an update checklist.
  Draft output.route_prompt only when the PM requests delegated application.
  Require exact PM approval, branch preflight, validation output, and draft PR review for terminal-agent writes.

OUTPUT:
  output.adoption_packet plus output.route_prompt when delegated update is explicitly requested.

LIMITS:
  No product-code, CI, package, deploy, runtime-config, secret-store, settings, release, tag, label, merge, or closure authority.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-0.5 verify-target-adoption after draft or delegated update.
