# MOS-5.15 execute-production-deploy

MOSDLC:
  ID: MOS-5.15
  Phase: Fase 5 - Despliegue local / staging / produccion
  Surface: actor.terminal_agent
  Compatibility source: none
  Classification: new
  Workflow: candidate (production execution by terminal agent not modeled; Human PM by default)
  Mode: candidate (Human PM by default)
  Output: output.execution_report
  Evidence: evidence.pm_approval, evidence.source_basis, evidence.target_adoption, evidence.validation_output, evidence.repo_state

OPERATION:
  Represent production deployment execution as a resolved decision: production is not executed by a terminal agent under the current kernel and stays with the Human PM by default.
  Source map summary: workflow.deployment and mode.delegated_deploy_execution cover only local and staging (MOS-5.11 y MOS-5.13). Production por agente no se modela; por defecto produccion queda con el Humano PM y requiere una ruta separada mas estricta antes de existir.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Candidate posture for production only: no workflow or mode id executes production deployment by terminal agent. workflow.deployment and mode.delegated_deploy_execution are internal-only and cover local and staging only; they never execute production.
  Resolved decision (durable, no longer ambiguous): production deploy by agent stays fail-closed candidate-only; a stricter, separately approved production path is the named prerequisite. See docs/decisions/0001-fase5-deploy-execution-fail-closed.md.
  Emit output.execution_report only to report the fail-closed candidate result. Apply boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, boundary.separate_pm_approval, and boundary.validation_discipline.

COMPATIBILITY_SOURCE:
  No 00-37 compatibility source is mapped for this Fase 5 operation.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read target-owned production deploy notes, exact PM approval evidence, adoption state, source basis, and validation evidence live only to confirm that production execution by agent must fail closed and stay with the Human PM.
  Exact PM deploy approval alone does not convert production into a terminal-agent-executable operation under the current kernel; production remains with the Human PM by default.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Report the candidate status for production, the missing stricter-path prerequisite, required target-owned command evidence, secret-safety posture, and the safe Human PM route.
  Recommend MOS-5.14 when a production command bundle must be drafted for Human PM execution, or MOS-R.13 after Human PM production deployment.
  Redact sensitive values as [REDACTED] and reference only variable names, command names, file paths, and risk types.
  Do not execute production deployment, run deploy commands, request secrets, print environment values, mutate config, mutate GitHub, change host/DNS/provider/payment/auth settings, or claim production deploy success.
  Do not run broad environment/config dumps such as env, printenv, or set.

OUTPUT:
  output.execution_report stating that production deploy execution is fail-closed candidate-only and Human PM by default under the current kernel, with evidence reviewed and safe next step.

LIMITS:
  Candidate template only for production; no production deploy execution by agent, and no repository, GitHub, runtime-config, secret-store, database, host, DNS, provider, payment/auth, release, or external-service mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-R.13 after Human PM production deployment; otherwise MOS-5.14 or MOS-R.3.
