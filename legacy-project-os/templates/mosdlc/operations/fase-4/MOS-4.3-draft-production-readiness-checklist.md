# MOS-4.3 draft-production-readiness-checklist

MOSDLC:
  ID: MOS-4.3
  Phase: Fase 4 - Testing / QA
  Surface: actor.browser_chat
  Compatibility source: templates/operations/18-draft-human-qa-checklist.md
  Classification: variant; merge-candidate (con MOS-4.1 vía alcance readiness)
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state

OPERATION:
  Draft a human production-readiness QA checklist without executing deployment or release work.
  Source map summary: Draftea el checklist humano de QA de production readiness. Verificar preparación real antes de considerar producción. Checklist transversal de readiness verificable por un humano.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>   # optional
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/18-draft-human-qa-checklist.md as compatibility source for this Fase 4 operation shape.
  Do not delete, rename, renumber, or bypass the 18 compatibility template.

LIVE_STATE:
  Read repository state, adoption notes, requirements, risk notes, and relevant docs live.
  Treat production readiness as QA/readiness classification, not deployment authorization or execution.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft human-verifiable readiness checks for functionality, docs, security posture, configuration hygiene, observability, rollback awareness, and known blockers.
  Redact secret-looking values as [REDACTED] and report only paths, variable names, and risk types when sensitive configuration is relevant.
  Return status.needs_context when repository or readiness basis is insufficient.
  Do not draft deploy commands, execute deployment, add deployment workflow ids, or claim production readiness is complete.

OUTPUT:
  output.status_result carrying the drafted production-readiness QA checklist or the fail-closed status.

LIMITS:
  Draft-only/read-only readiness checklist drafting; no QA execution, no deployment behavior, no repository or GitHub mutation, and no claim that human QA was completed.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-4.6.
