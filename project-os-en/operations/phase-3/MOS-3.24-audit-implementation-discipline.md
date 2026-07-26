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
- Optional: TARGET_REPOSITORY, AUDIT_SCOPE, PATH_SCOPE, FOCUS, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are human context only and never authorize an action)

**Alternative locators and human constraints:** `TARGET_REPOSITORY` and
`AUDIT_SCOPE` are alternative locators, never cumulative requirements. First
reuse an unambiguous source already selected. Without one, a deliberately
repo-wide audit asks for `TARGET_REPOSITORY`; a scoped audit asks for
`AUDIT_SCOPE` —an issue or PR— and derives the repository and the remaining
verifiable relations from that source. `PATH_SCOPE` and `FOCUS` are optional
human constraints, not derived metadata. If no sufficient source exists, or
both locators are declared and resolve to incompatible targets, fail closed with
`status.needs_context`; never select a target or mix evidence.

**Deliver:** output.review_result (+output.draft_issue). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: any phase. Next: MOS-3.14. Recommended: MOS-3.14.
