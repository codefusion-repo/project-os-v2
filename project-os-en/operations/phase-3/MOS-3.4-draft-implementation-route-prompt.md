# MOS-3.4 — Draft implementation route prompt

MOSDLC operation `draft-implementation-route-prompt` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (the route prompt does not authorize; writing requires exact PM approval)

**Does:** Draft the route-prompt to delegate the implementation of an issue to a terminal agent.
**For:** To route implementation with correct scope, mode and evidence.
**How:** Use a compact bootloader. Browser chat may recommend an optional skill and infer `RECOMMENDED_TERMINAL_AGENT_FAMILY` from the work. The recommendation is advisory, authorizes nothing, and may be overridden by explicit PM feedback.

**Variables**
- Required: — (none)
- Optional: ISSUE_NUMBER, ROADMAP_ISSUE, OPTIONAL_SKILL, HYDRATION_LEVEL, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (the skill, level, PM feedback, and PM questions are context only and never authorize an action). `HYDRATION_LEVEL` accepts `minimal`, `compact` (default), or `full/debug` and controls only the resolver's hydrated content. The wizard requires `PM_AUTHORIZATION_STATUS` and preloads `HYDRATION_LEVEL=compact` before generating this route prompt.

**Deliver:** output.route_prompt. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.1, MOS-3.2 or MOS-3.8. Next: MOS-3.7 after the PR. Recommended: MOS-3.7.
