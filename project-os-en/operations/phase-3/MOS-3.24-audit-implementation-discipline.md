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
- Required: TARGET_REPOSITORY
- Optional: PATH_SCOPE, FOCUS, AUDIT_SCOPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Derived metadata:** `TARGET_REPOSITORY`, `PATH_SCOPE`, `FOCUS`, and
`AUDIT_SCOPE` represent different scope levels, so their precedence is
explicit: (1) use the source the current invocation already selected; (2) if
none exists, one supplied primary locator —`AUDIT_SCOPE` accepts the issue or
the PR that narrows the audit; (3) derive the rest of the metadata and scope
from it; (4) return the decision to the PM only when several material
interpretations are equally valid. `TARGET_REPOSITORY` is kept because a
deliberately repo-wide audit has no other source of reach; the issue and the PR
are never asked for together.

**Deliver:** output.review_result (+output.draft_issue). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: any phase. Next: MOS-3.14. Recommended: MOS-3.14.
