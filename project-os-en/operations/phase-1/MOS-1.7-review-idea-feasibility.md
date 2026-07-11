# MOS-1.7 — Review idea feasibility

MOSDLC operation `review-idea-feasibility` · Phase 1 — Requirements, planning, and feasibility · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Evaluate a new idea as a possible project requirement.
**For:** Decide if the idea fits into the roadmap.
**How:** Analyzes the idea against live status and documentation and recommends route.

**Variables**
- Required: IDEA
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: any phase. Next: MOS-1.8 if applicable. Recommended: MOS-1.8.
