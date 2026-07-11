# MOS-3.5 — Draft correction route prompt

MOSDLC operation `draft-correction-route-prompt` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (the route prompt does not authorize; writing requires exact PM approval)

**Does:** Draft a non-authorizing correction route prompt from actionable PR or issue feedback without expanding scope.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Summarize actionable findings and map each one to the original issue or PR evidence.

**Variables**
- Required: ISSUE_NUMBER
- Optional: PR_NUMBER, OPTIONAL_SKILL, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.route_prompt. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.7, MOS-3.25, MOS-4.4. Next: MOS-3.7. Recommended: MOS-3.7.
