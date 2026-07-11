# MOS-4.2 — Draft qa checklist description

MOSDLC operation `draft-qa-checklist-description` · Phase 4 — QA and human verification · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Draft a human QA checklist from a stable feature description without executing QA.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Convert DESCRIPTION into human-verifiable QA steps, expected observations, and ambiguity notes.

**Variables**
- Required: DESCRIPTION
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: none. Next: MOS-4.5. Recommended: MOS-4.5.
