# Solicitar Revisión de Seguridad OWASP

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.security_revision, mode.review_only.
  Recipient is a real security-review specialist: a recipient/focus, not an actor surface.

INPUT:
  PR_NUMBER=<PR_NUMBER>

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the source context cannot be read without exposing secrets.

LIVE_STATE:
  Read live: the PR_NUMBER diff and sensitive components, plus repository context, without exposing secrets.

DO:
  Identify security-sensitive surfaces (auth, authorization, sessions/cookies, input validation, file uploads,
  redirects, dependencies, admin paths, secrets handling, logging, error exposure, deployment/config risk).
  Draft an OWASP-based security-review prompt with redaction requirements and concrete evidence to inspect.

OUTPUT:
  output.security_review_prompt that routes the review only.

LIMITS:
  Never ask anyone to print, paste, upload, quote, summarize, or expose .env, tokens, credentials, cookies, JWTs,
  private keys, CI secrets, database URLs, or secret-looking values; require [REDACTED].
  Runs no scanner and approves no insecure code; the recipient is not an actor.


RECOMMENDED_NEXT_OPERATION:
  External security reviews, then Operation 08 (Draft correction) if findings exist.
