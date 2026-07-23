# MOS-3.5 — Draft correction route prompt

MOSDLC operation `draft-correction-route-prompt` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (the route prompt does not authorize; writing requires exact PM approval)

**Does:** Draft the correction route-prompt of a live work unit from findings
with a `blocking-correction` disposition.
**For:** To correct only material breaches without expanding the original scope.
**How:** Encapsulate only `blocking-correction` findings in a delegated
correction route; `non-blocking-follow-up` findings defer to MOS-3.3, and
`preference`, `accepted-risk`, and `invalid-finding` force no changes. Fill
`WORK_UNIT` with the corrected live unit and keep its `CHANGE_CLASS`. Carry the
exact reference to the source review or comment (`SOURCE_REVIEW`) and, when the
unit corrects an existing PR, its `PR_NUMBER`; both are mandatory and never
invented. The route prompt requires the executing agent to publish exactly one
append-only correction report on that PR that references the source review,
records the previous and corrected heads, maps each `blocking-correction` to its
outcome, identifies the commits or range and the real validation, states
remaining work, and confirms no merge or close happened, without editing the body
or any prior comment. Findings travel by intent: the material breach and its
observable criterion are binding; the reviewer's wording and solution proposals
are advisory. Browser chat may recommend an optional skill and infer
`RECOMMENDED_TERMINAL_AGENT_FAMILY` from the work. The recommendation is
advisory, authorizes nothing, and may be overridden by explicit PM feedback.

**Variables**
- Required: WORK_UNIT, SOURCE_REVIEW, PR_NUMBER, CHANGE_CLASS
- Optional: OPTIONAL_SKILL, HYDRATION_LEVEL, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (the skill, level, PM feedback, and PM questions are context only and never authorize an action). `HYDRATION_LEVEL` accepts `minimal`, `compact`, or `full/debug`; it controls the resolver's hydrated content and applies the contractual PM-facing receipt visibility without altering the internal receipt or `context_plan`. The wizard requires `PM_AUTHORIZATION_STATUS` and preloads `HYDRATION_LEVEL` with the declared `CHANGE_CLASS` contractual density (`full/debug` for `change_class.critical`), never below it.

**Deliver:** output.route_prompt. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.7, MOS-3.25 or MOS-4.4, only with
`blocking-correction` findings. Next: MOS-3.7. Recommended: MOS-3.7.
