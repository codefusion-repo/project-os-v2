# MOS-3.27 — Review project state and verify postconditions

MOSDLC operation `review-project-state` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.review_result (+output.status_result)
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Review project status within a scoped reference and, when an executed
action with its expected postconditions is declared, verify them one by one
against live evidence.
**For:** To detect drift between docs, roadmap and repo reality within that
reference, and to confirm that a declared action (merge, tag, close, deploy)
left the expected state.
**How:** Reconstruct and preserve the live unit's `CHANGE_CLASS` while verifying,
without asking for it as a manual PM input: a critical unit is verified as
`change_class.critical`, `review.independent`, `validation.broad`,
and the critical report density, while its normal hydration is
`compact` and only changes through an explicit override. `REVIEWED_REFERENCE`
is the single primary locator and scopes both review modes. Without
`ACTION_EXECUTED`, use `REVIEWED_REFERENCE` to scope which PM decisions and
fixed docs to contrast against live evidence, and report drift only within
that reference. With `ACTION_EXECUTED`, `REVIEWED_REFERENCE`, and
`EXPECTED_POSTCONDITIONS`, verify each postcondition against the corresponding
live evidence —effective merge, the main branch's final SHA, correspondence with
the reviewed head, post-merge checks, unit closure, remote branch deletion, and
local cleanup— and report the state of each. `ACTION_EXECUTED` and
`EXPECTED_POSTCONDITIONS` only select and scope the verification mode; they are
never additional locators and never widen the reviewed surface. It runs no
mutation; an unmet or unverifiable postcondition fails closed.

**Variables**
- Required: — (none)
- Optional: ACTION_EXECUTED, REVIEWED_REFERENCE, EXPECTED_POSTCONDITIONS, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (declaring the first three enables postcondition verification; PM feedback and questions are context only and never authorize an action)

**Single locator and human constraints:** `REVIEWED_REFERENCE` is the only
primary locator for MOS-3.27 in both modes and is never combined with another
locator in routine capture. First reuse an unambiguous source already selected
in the execution context; in that case `REVIEWED_REFERENCE` may be empty.
Without sufficient context, supply exactly one verifiable live reference —a
work unit, PR, roadmap, or equivalent record— and derive the repository and
the remaining verifiable relations from it; a full repository is only the
reference when the PM or a live unit selects it explicitly, never by default.
`ACTION_EXECUTED` and `EXPECTED_POSTCONDITIONS` only select and scope the
verification mode; they never substitute for or widen `REVIEWED_REFERENCE`.
Without `REVIEWED_REFERENCE` or an unambiguous context source, or when its
format is not verifiable, fail closed with `status.needs_context` instead of
reviewing the whole repository, its issues, or its history. Two currently
valid, materially incompatible references return `status.needs_context` or,
for verifiably conflicting PM decisions, `status.needs_pm_decision`; it never
picks one or mixes evidence from both.

**Deliver:** output.review_result (+output.status_result). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: any phase; MOS-3.7, MOS-3.11, or a deploy to verify their postconditions. Next: MOS-3.1, MOS-3.3 or MOS-R.9. Recommended: MOS-R.9 if the drift is documentary.
