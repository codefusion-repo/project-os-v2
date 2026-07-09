# MOS-6.1 review-security-production-readiness

MOSDLC:
  ID: MOS-6.1
  Phase: Fase 6 - Maintenance and tooling
  Surface: actor.browser_chat
  Compatibility source: templates/operations/20-request-owasp-security-review.md, templates/operations/25-audit-implementation-discipline-gaps.md
  Classification: new
  Workflow: workflow.review_only
  Mode: mode.review_only
  Output: output.status_result
  Evidence: evidence.repo_state

OPERATION:
  Review security for production readiness across the current project state.
  Source map summary: Revisa la seguridad del proyecto para production readiness. Detectar riesgos de seguridad antes de producción. Revisión read-only OWASP y 8 dominios sobre el estado actual.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.review_only with mode.review_only and emit only the declared output contracts.
  Apply boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, and boundary.fail_closed.

COMPATIBILITY_SOURCE:
  Use templates/operations/20-request-owasp-security-review.md and templates/operations/25-audit-implementation-discipline-gaps.md as compatibility sources for this Fase 6 operation shape.
  Do not delete, rename, renumber, or bypass the 20 or 25 compatibility templates.

LIVE_STATE:
  Read TARGET_REPOSITORY code, dependencies, configuration surfaces, and prior security findings live.
  Treat production readiness as an advisory review, not a release decision.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Review authentication, authorization, sessions/cookies, input validation, file uploads, redirects, dependency risk, admin surfaces, secrets handling, logging, and error exposure against OWASP and the 8 security domains.
  Map every finding to concrete file paths, variable names, or risk types; redact values as [REDACTED].
  Classify findings by severity and whether they block production readiness.
  Return status.needs_context when TARGET_REPOSITORY evidence cannot be inspected.
  Do not run scanners, request secret values, run broad environment/config dumps such as env, printenv, set, framework config dumps, or CI secret-context dumps, or claim production security readiness is complete.

OUTPUT:
  output.status_result carrying the security production-readiness findings, severities, and safe recommended next operation.

LIMITS:
  Read-only security review; no repository, GitHub, settings, runtime-config, secret-store, or deployment mutation.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-6.7.
