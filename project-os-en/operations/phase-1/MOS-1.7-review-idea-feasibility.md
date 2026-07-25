# MOS-1.7 — Review idea feasibility

MOSDLC operation `review-idea-feasibility` · Phase 1 — Requirements, planning, and feasibility · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Evaluate a new idea and pick its risk-proportional route.
**For:** To decide what to do with the idea: implement it directly, split it
into slices, investigate or prototype it, record it as a durable decision,
update only the roadmap, or reject or defer it.
**How:** Analyze the idea against live status and documentation, then recommend
one of those routes by risk and concreteness; a concrete, bounded idea may go
straight to implementation without passing through documentation or roadmap.

**Variables**
- Required: IDEA
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: any phase. Next: the chosen route — MOS-3.8 or
MOS-3.4 to implement, MOS-3.2 for slices, MOS-R.1 for a durable decision,
MOS-1.12 for roadmap only, MOS-1.8 only when docs or roadmap became stale, or
none when rejected or deferred. Recommended: the chosen proportional route.
