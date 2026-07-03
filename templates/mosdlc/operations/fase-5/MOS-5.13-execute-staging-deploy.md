# MOS-5.13 execute-staging-deploy

MOSDLC:
  ID: MOS-5.13
  Phase: Fase 5 - Despliegue local / staging / produccion
  Surface: actor.terminal_agent
  Compatibility source: none
  Classification: new
  Workflow: candidate (no current kernel workflow id)
  Mode: candidate (no current kernel execution mode id)
  Output: output.execution_report
  Evidence: evidence.pm_approval, evidence.source_basis, evidence.target_adoption, evidence.validation_output, evidence.repo_state

OPERATION:
  Represent staging deployment execution as a kernel-candidate surface that fails closed under the current kernel and does not execute deployment.
  Source map summary: Ejecuta despliegue staging por terminal agent solo si el target lo soporta. Ejecuta solo comandos target-owned bajo aprobacion exacta y reporta redactado. This migration preserves candidate posture and does not implement deploy-by-agent execution.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Candidate posture only: no current workflow or mode id is resolved for terminal-agent deploy execution.
  Use no new kernel ids in this template. Emit output.execution_report only to report the fail-closed candidate result.
  Apply boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, boundary.separate_pm_approval, and boundary.validation_discipline.

COMPATIBILITY_SOURCE:
  No 00-37 compatibility source is mapped for this Fase 5 operation.
  Do not delete, rename, renumber, or bypass any templates/operations/00-37 compatibility template.

LIVE_STATE:
  Read target-owned staging deploy notes, exact PM approval evidence, adoption state, source basis, and validation evidence live only to decide whether this candidate must fail closed.
  Exact PM deploy approval alone does not convert this candidate template into an executable operation under the current kernel.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Report candidate status, required missing kernel decision, required target-owned command evidence, secret-safety posture, and safe Human PM route.
  Recommend MOS-5.12 when a staging command bundle must be drafted for Human PM execution, or MOS-R.13 after Human PM staging deployment.
  Redact sensitive values as [REDACTED] and reference only variable names, command names, file paths, and risk types.
  Do not execute staging deployment, run deploy commands, request secrets, print environment values, mutate config, mutate GitHub, change host/DNS/provider settings, run broad environment/config dumps, or claim staging deploy success.

OUTPUT:
  output.execution_report stating that staging deploy execution is fail-closed candidate-only under the current kernel, with evidence reviewed and safe next step.

LIMITS:
  Candidate template only; no deploy execution, no command execution, and no repository, GitHub, runtime-config, secret-store, database, host, DNS, provider, payment/auth, or external-service mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-R.13 after Human PM staging deployment; otherwise MOS-5.12 or MOS-R.3.
