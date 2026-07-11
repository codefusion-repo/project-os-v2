# MOS-1.1 — Interview requirements

MOSDLC operation `interview-requirements` · Phase 1 — Requirements, planning, and feasibility · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result
- Evidence: evidence.source_basis
- PM approval: No (draft-only)

**Does:** Conduct a guided interview with the PM to elicit requirements.
**For:** To capture functional and non-functional requirements from the PM's knowledge.
**How:** Ask iterative questions in chat and synthesize the findings without writing files.

**Variables**
- Required: — (none)
- Optional: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-0.5. Next: MOS-1.2. Recommended: MOS-1.2.
