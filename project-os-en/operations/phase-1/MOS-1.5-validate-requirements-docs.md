# MOS-1.5 — Validate requirements docs

MOSDLC operation `validate-requirements-docs` · Phase 1 — Requirements, planning, and feasibility · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (read-only)

**Does:** Validate requirements documentation against identified requirements before roadmap planning.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Check coverage, contradictions, missing non-functional requirements, unclear use cases, missing user stories, and unresolved PM decisions.

**Variables**
- Required: — (none)
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-1.4. Next: MOS-1.6. Recommended: MOS-1.6.
