# MOS-3.7 — Review PR before close

MOSDLC operation `review-pr-before-close` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_before_close · mode.review_only · output.review_result (+output.pm_command_bundle)
- Evidence: evidence.issue_scope, evidence.pr_diff, evidence.validation_output
- PM approval: No (does not merge or close; drafts closure only after a resolved review)

**Does:** Review the PR against the linked issue, classify every finding by
disposition, and on a GO verdict deliver the closeout in the same response.
**For:** Quality gate prior to any closure, without redundant turns.
**How:** Compare the diff, validation, and scope; use execution reports as
evidence leads. Classify every finding as `blocking-correction`,
`non-blocking-follow-up`, `preference`, `accepted-risk`, or `invalid-finding`;
only `blocking-correction` returns to correction. On GO, draft the complete
closeout bundle and its final verification in the same response.

**Variables**
- Required: PR_NUMBER
- Optional: EXECUTION_REPORT, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.review_result (+output.pm_command_bundle). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.4 or MOS-3.5. Next: on GO the closeout goes in
the same response and MOS-3.6 remains only as exceptional regeneration;
MOS-3.5 only with `blocking-correction` findings; non-blocking follow-ups to
MOS-3.3. Recommended: MOS-3.5 only when there is a `blocking-correction`.
