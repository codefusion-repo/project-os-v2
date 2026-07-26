# MOS-3.24 — Audit implementation discipline

MOSDLC operation `audit-implementation-discipline` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.implementation_discipline_audit · mode.review_only · output.review_result (+output.draft_issue)
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Audit implementation discipline gaps against boundary.implementation_discipline.
**For:** To detect discipline debt with file and line evidence.
**How:** Read-only audit with findings and follow-up drafts.

**Variables**
- Required: — (none)
- Optional: AUDIT_SCOPE, PATH_SCOPE, FOCUS, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are human context only and never authorize an action)

**Single locator and human constraints:** `AUDIT_SCOPE` is the only primary
locator and is never combined with another locator in routine capture. First
reuse an unambiguous source already selected; in that case `AUDIT_SCOPE` may be
empty. Without sufficient context, supply exactly one verifiable reference:
`owner/repo` for a repo-wide audit, or an issue or PR for a scoped audit. Derive
the repository and the remaining verifiable relations from that source or the
context. `PATH_SCOPE` and `FOCUS` are optional human constraints, not derived
metadata. If a locator and sufficient context are both absent, its format is not
verifiable, or the evidence resolves incompatible sources, fail closed with
`status.needs_context`; never select a target or mix evidence.

**Deliver:** output.review_result (+output.draft_issue). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: any phase. Next: MOS-3.14. Recommended: MOS-3.14.
