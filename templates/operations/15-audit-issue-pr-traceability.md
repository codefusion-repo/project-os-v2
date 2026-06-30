# Auditar Trazabilidad de Issues y PRs

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.review_only, mode.review_only.
  A terminal agent may run the read-only auditor (tools.audit_traceability) against live GitHub state.

INPUT:
  ISSUE_NUMBER=<ISSUE_NUMBER>

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the issue history cannot be read.

LIVE_STATE:
  Read live: ISSUE_NUMBER comment history, labels, linked PRs, and commits.
  Compare against docs/TRACEABILITY_PROTOCOL.md.

DO:
  Verify closure evidence and complete traceability so the GitHub-based memory stays stable.
  Report gaps: missing PM decision, missing execution report, missing closure comment, and the like.

OUTPUT:
  output.status_result naming the traceability gaps with evidence references.

LIMITS:
  Read-only audit; never rewrites past comments or edits history.


RECOMMENDED_NEXT_OPERATION:
  If gaps found, Operation 08 (Draft correction) or 21 (Draft follow-up).
