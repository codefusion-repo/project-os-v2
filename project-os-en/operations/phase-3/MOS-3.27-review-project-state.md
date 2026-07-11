# MOS-3.27 — Review project state

MOSDLC operation `review-project-state` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Review project state and documentation alignment from live repository and PM decision evidence.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Compare current repository, roadmap, docs, issues, and PR state against stable PM decisions and source docs.

**Variables**
- Required: — (none)
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: none. Next: MOS-3.1, MOS-3.3, MOS-R.9. Recommended: MOS-R.9.
