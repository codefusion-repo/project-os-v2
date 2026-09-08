# MOS-3.7 — Review PR before close

MOSDLC operation `review-pr-before-close` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_before_close · mode.review_only · output.review_result (+output.pm_command_bundle)
- Evidence: evidence.issue_scope, evidence.pr_diff, evidence.validation_output
- PM approval: No (does not merge or close; drafts closure only after a resolved review)

**Does:** Review the change against its live unit, classify every finding by
disposition, and on a GO verdict deliver the closeout in the same response.
**For:** Quality gate prior to any closure, without redundant turns.
**How:** Compare the diff, validation, and scope; use execution reports as
evidence leads. Reconstruct the live unit's `CHANGE_CLASS` from its evidence —not
asked as a manual PM input— and resolve the review at that class: a critical unit
keeps `change_class.critical`, `review.independent`, `validation.broad`,
and the critical report density, while its normal hydration is `compact`
and only changes through an explicit override. Read findings by intent:
the material breach is binding, the proposed solution is advisory.
Before treating an observation as a finding, apply
the materiality gate from `rule.economia_de_contexto`: it requires a verifiable
current state, an unsatisfied outcome, contract, risk, or capability, a concrete
materially improving action, and durable value; something merely historical,
informational, confirmatory, already resolved by the normal course, or duplicated
is not a finding and is omitted, or `invalid-finding` without routing if already
raised. Only then classify every finding as `blocking-correction`,
`non-blocking-follow-up`, `preference`, `accepted-risk`, or `invalid-finding`; a
`non-blocking-follow-up` requires a current, durable, actionable gap with
independent scope and a reason to defer it, and only `blocking-correction`
returns to correction via MOS-3.5. Every correction of this PR is recorded as an
append-only correction report —source review, previous head, corrected head,
findings addressed, and validation— without editing the body or prior comments,
and feeds a new MOS-3.7 over the corrected head. On GO, the resolved review is
the closeout gate: deliver the complete bundle of ready when applicable, merge,
closure, and cleanup directly in the same response, with final read-only
verification, following `project-os-en/templates/pm-command-bundle.md`.
Do not request another round of PM approval per action to deliver that bundle.
The human PM executes it; `browser_chat` never executes those actions and GO
does not delegate their execution to the agent. This rule is limited to
`workflow.review_before_close`; implementation, correction, deploy, release,
settings, and all other workflows retain their exact approvals.

If that bundle is lost, becomes stale, or the closure fails, run this operation
again over the current evidence to regenerate it; a later independent
postcondition verification uses MOS-3.27.

Reconstruct the same primary unit and PR when receiving review, QA, or a
correction report. Pending or failed required manual QA prevents GO: use
MOS-4.1/MOS-4.4 to complete it within that unit. Closeout creates no additional
unit and cannot omit blockers or validate a previous head.

**Variables**
- Required: PR_NUMBER
- Optional: EXECUTION_REPORT, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.review_result (+output.pm_command_bundle with resolved GO).
If evidence or scope is missing or ambiguous, validation fails, or a review
gate remains pending, fail closed with output.status_result. Do not turn
bundle delivery after GO into a new request for PM approval per action.

**Connections:** Previous: MOS-3.4 or MOS-3.5. Next: on GO the closeout and its
verification go in the same response; MOS-3.5 only with `blocking-correction`
findings; non-blocking follow-ups to MOS-3.3; later independent verification
with MOS-3.27. Recommended: MOS-3.5 only when there is a `blocking-correction`.
