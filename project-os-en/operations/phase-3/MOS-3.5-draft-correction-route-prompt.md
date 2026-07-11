# MOS-3.5 — Draft correction route prompt

MOSDLC operation `draft-correction-route-prompt` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (the route prompt does not authorize; writing requires exact PM approval)

**Does:** Draft the correction route-prompt of a PR/issue from actionable feedback.
**For:** To correct without expanding the original scope.
**How:** Encapsulate findings in a delegated correction route. Browser chat may recommend an optional skill and infer `RECOMMENDED_TERMINAL_AGENT_FAMILY` from the work. The recommendation is advisory, authorizes nothing, and may be overridden by explicit PM feedback.

**Variables**
- Required: ISSUE_NUMBER
- Optional: PR_NUMBER, OPTIONAL_SKILL, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (the skill, PM feedback, and PM questions are context only and never authorize an action). The wizard requires `PM_AUTHORIZATION_STATUS` before generating this route prompt.

**Deliver:** output.route_prompt. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.7, MOS-3.25 or MOS-4.4. Next: MOS-3.7. Recommended: MOS-3.7.
