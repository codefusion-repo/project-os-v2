# MOS-R.19 plan-validation-cycle

MOSDLC:
  ID: MOS-R.19
  Phase: Operaciones recomendadas aceptadas (transversal)
  Surface: actor.browser_chat to actor.human_pm
  Compatibility source: none
  Classification: accepted-recommended; new
  Workflow: workflow.pm_intake
  Mode: mode.review_only
  Output: output.draft_issue, output.pm_command_bundle
  Evidence: evidence.source_basis, evidence.repo_state

OPERATION:
  Plan a real validation cycle for the target project, drafting the plan and its bounded issues for Human PM execution.
  Source map summary: Planifica un ciclo de validación real del target según el tipo de proyecto. Probar el producto end-to-end con evidencia real antes de ampliarlo o publicarlo. Draftea el plan y los issues acotados del ciclo; falla cerrado si el target no tiene superficie de validación aplicable.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  VALIDATION_CYCLE_TYPE=<VALIDATION_CYCLE_TYPE>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

  VALIDATION_CYCLE_TYPE names the validation surface that fits the target project type, for example:
  - web apps: internal QA, staging validation, beta rollout, UAT;
  - mobile apps: TestFlight/internal testing, release candidate validation;
  - games: playtest, balance test, content QA, performance validation;
  - libraries/tools: integration test, consumer validation, release candidate trial;
  - internal systems: pilot rollout, acceptance test, operational validation.

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.pm_intake with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  No 00-37 compatibility source is mapped for this recommended operation.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  This operation depends on the target actually having an applicable validation surface; not every target project has staging, beta channels, playtests, or pilots. Read the target's docs, roadmap, and adoption notes live to identify the applicable surface, and fail closed to status.needs_context when none applies.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft the validation-cycle plan for the applicable surface: goals, entry criteria, bounded scope, participants or evidence sources, exit criteria, and how findings will be captured.
  Draft the cycle's bounded issues as output.draft_issue content and the Human PM-executed creation commands as output.pm_command_bundle.
  Return status.needs_context when the target's validation surface cannot be identified, and status.needs_pm_decision when the PM must choose between applicable validation surfaces.
  Do not create issues, start the cycle, contact participants, or execute any command.

OUTPUT:
  output.draft_issue content for the cycle's bounded issues plus output.pm_command_bundle for Human PM-executed creation, or a fail-closed status when no validation surface applies.

LIMITS:
  Draft-only planning; the Human PM decides and executes the bundle and owns cycle start.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-R.20.
