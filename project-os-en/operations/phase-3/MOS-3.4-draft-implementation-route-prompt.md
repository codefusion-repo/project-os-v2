# MOS-3.4 — Draft implementation route prompt

MOSDLC operation `draft-implementation-route-prompt` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (the route prompt does not authorize; writing requires exact PM approval)

**Does:** Draft a non-authorizing route prompt for delegated terminal-agent implementation of one scoped issue.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft output.route_prompt with exact repository, issue, branch naming expectation, workflow.issue_implementation, execution mode, proportional validation expectations, and PM_AUTHORIZATION_STATUS.

**Variables**
- Required: — (none)
- Optional: ISSUE_NUMBER, ROADMAP_ISSUE, OPTIONAL_SKILL, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.route_prompt. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.1, MOS-3.2, MOS-3.8. Next: MOS-3.7. Recommended: MOS-3.7.
