# MOS-3.24 — Audit implementation discipline

MOSDLC operation `audit-implementation-discipline` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.review_result
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Audit implementation discipline with an explicit focus on the three
active boundaries: boundary.implementation_discipline,
boundary.primary_path_discipline, and boundary.validation_discipline.
**For:** To detect discipline debt with file and line evidence, without a
specialized workflow of its own.
**How:** Read-only audit over `workflow.review_only` that delivers findings
with a verifiable disposition; downstream processing lives in MOS-3.14, never
in a direct issue delivery.

**Variables**
- Required: — (none)
- Optional: AUDIT_SCOPE, PATH_SCOPE, FOCUS, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are human context only and never authorize an action)

**Single locator and human constraints:** `AUDIT_SCOPE` is the only primary
locator and is never combined with another locator in routine capture. First
reuse an unambiguous source already selected; in that case `AUDIT_SCOPE` may be
empty. Without sufficient context, supply exactly one verifiable reference:
`owner/repo` for a repo-wide audit, or an issue or PR for a scoped audit. Derive
the repository and the remaining verifiable relations from that source or the
context. `PATH_SCOPE` is an optional human constraint that narrows surface, not
derived metadata. `FOCUS` can only narrow the analysis within the three
discipline boundaries; it never widens scope or selects another workflow. If a
locator and sufficient context are both absent, its format is not verifiable,
or the evidence resolves incompatible sources, fail closed with
`status.needs_context`; never select a target or mix evidence.

**Deliver:** output.review_result. Findings are not delivered as a direct
issue: MOS-3.14 classifies them and routes to correction, follow-up, or no-op.
If evidence, scope, or approval is missing or ambiguous, fail closed: report
with `output.status_result` and return the decision to the PM.

**Connections:** Previous: any phase. Next: MOS-3.14. Recommended: MOS-3.14.
