# MOS-3.23 request-security-review

MOSDLC:
  ID: MOS-3.23
  Phase: Fase 3 - Development / Implementation
  Surface: actor.browser_chat to external_recipient
  Compatibility source: templates/operations/20-request-owasp-security-review.md
  Classification: replacement
  Workflow: workflow.security_revision
  Mode: mode.review_only
  Output: output.security_review_prompt
  Evidence: evidence.repo_state, evidence.source_basis

OPERATION:
  Draft an external-recipient security review prompt with strict secret-redaction posture.
  Source map summary: Draftea el prompt de revisión de seguridad OWASP y de los 8 dominios donde corresponda. Obtener un gate de seguridad externo con redacción obligatoria. Prompt con superficie sensible descrita sin exponer secretos.

INPUT:
  PR_NUMBER=<PR_NUMBER>
  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional
  PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Use workflow.security_revision with mode.review_only and emit only the declared output contracts.
  Apply boundary.draft_only_browser, boundary.output_not_permission, boundary.no_live_state_durable, boundary.no_invented_state, boundary.security_privacy, boundary.fail_closed, and boundary.separate_pm_approval.

COMPATIBILITY_SOURCE:
  Use templates/operations/20-request-owasp-security-review.md as compatibility source for this Fase 3 operation shape.
  Do not delete, rename, renumber, or bypass the 20 compatibility template.

LIVE_STATE:
  Read PR, issue, repository context, sensitive surfaces, and PM-provided security scope live without exposing secrets.
  Treat the security reviewer as an external recipient only, not as a kernel actor.
  Store no issue, PR, branch, commit, validation, release, deployment, or planning state in durable files.

DO:
  Draft output.security_review_prompt with review objective, sensitive surfaces, OWASP areas, the eight security domains where relevant, evidence to inspect, findings format, and redaction rules.
  Require all secret-looking values to be redacted as [REDACTED] and never request .env, tokens, credentials, cookies, JWTs, database URLs, CI secrets, private keys, or production settings.
  Do not run scanners, upload code, expose hidden environment values, or create new kernel actors.
  Preserve external-recipient posture; the recipient is not a kernel actor.
  Apply strict secret redaction; report only paths, variable names, risk types, and [REDACTED] placeholders when sensitive values appear.

OUTPUT:
  output.security_review_prompt for an external recipient, or output.status_result when review context cannot be inspected safely.

LIMITS:
  Security-review prompt drafting only; external reviewers are not kernel actors and this template runs no scanners and exposes no secrets.
  Template authority: none. Exact PM approval plus kernel gates are required before any separate write-capable operation.
  PM_FEEDBACK_HUMANO and PM_QUESTION_HUMANO are optional context only.

RECOMMENDED_NEXT_OPERATION:
  MOS-3.25.
