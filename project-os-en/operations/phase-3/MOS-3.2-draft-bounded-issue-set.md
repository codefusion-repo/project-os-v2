# MOS-3.2 — Draft bounded issue set

MOSDLC operation `draft-bounded-issue-set` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only; the Human PM decides and runs the bundle)

**Does:** Draft a bounded set of implementation issues from live traceability and roadmap evidence with an explicit PM-provided limit.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Use the explicit ROADMAP_ISSUE plus ISSUE_COUNT_LIMIT or SCOPE_LIMIT to split only bounded outcomes.

**Variables**
- Required: ROADMAP_ISSUE
- Optional: ISSUE_COUNT_LIMIT, SCOPE_LIMIT, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.pm_command_bundle. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-1.6. Next: MOS-3.4. Recommended: MOS-3.4.
