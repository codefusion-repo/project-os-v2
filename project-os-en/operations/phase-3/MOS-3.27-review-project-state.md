# MOS-3.27 — Review project state and verify postconditions

MOSDLC operation `review-project-state` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.review_result (+output.status_result)
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Review project status and, when an executed action with its expected
postconditions is declared, verify them one by one against live evidence.
**For:** To detect drift between docs, roadmap and repo reality, and to confirm
that a declared action (merge, tag, close, deploy) left the expected state.
**How:** Without `ACTION_EXECUTED`, use PM decisions and fixed docs as the main
truth and report drift. With `ACTION_EXECUTED`, `REVIEWED_REFERENCE`, and
`EXPECTED_POSTCONDITIONS`, verify each postcondition against the corresponding
live evidence —effective merge, the main branch's final SHA, correspondence with
the reviewed head, post-merge checks, unit closure, remote branch deletion, and
local cleanup— and report the state of each. It runs no mutation; an unmet or
unverifiable postcondition fails closed.

**Variables**
- Required: — (none)
- Optional: ACTION_EXECUTED, REVIEWED_REFERENCE, EXPECTED_POSTCONDITIONS, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (declaring the first three enables postcondition verification; PM feedback and questions are context only and never authorize an action)

**Deliver:** output.review_result (+output.status_result). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: any phase; MOS-3.7, MOS-3.11, or a deploy to verify their postconditions. Next: MOS-3.1, MOS-3.3 or MOS-R.9. Recommended: MOS-R.9 if the drift is documentary.
