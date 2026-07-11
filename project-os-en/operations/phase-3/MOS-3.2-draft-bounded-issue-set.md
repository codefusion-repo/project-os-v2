# MOS-3.2 — Draft bounded issue set

MOSDLC operation `draft-bounded-issue-set` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only; the Human PM decides and runs the bundle)

**Does:** Draft a limited set of issues from live traceability and roadmap.
**For:** To plan work lots with explicit limit.
**How:** Demand a limit and draft one bundle per outcome.

**Variables**
- Required: ROADMAP_ISSUE
- Optional: ISSUE_COUNT_LIMIT, SCOPE_LIMIT, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.pm_command_bundle. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-1.6. Next: MOS-3.4 for each approved issue. Recommended: MOS-3.4.
