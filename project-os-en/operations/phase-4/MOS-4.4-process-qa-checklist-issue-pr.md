# MOS-4.4 — Process an issue/PR QA checklist

MOSDLC operation `process-qa-checklist-issue-pr` · Phase 4 — QA and human verification · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Process the issue/PR human-checklist result.
**For:** To convert human QA into correction, follow-up or advancement.
**How:** Apply the materiality gate and dispositions from MOS-3.7 to the QA
result for the same unit: `blocking-correction` consumes MOS-3.5;
`non-blocking-follow-up` consumes MOS-3.3, with grouping and independence;
`preference`, `accepted-risk`, and `invalid-finding` create no work. Deliver the
applicable canonical output in the same response without another selection or
locator. Execute no mutations. Pending or failed required QA prevents GO;
satisfied QA allows returning to MOS-3.7 with its evidence, without creating a
unit or replacing review or closeout authorization.

Deliver that evidence with covered criteria/dispositions, ref, and environment,
and what is reused or pending renewal under the common contract. When the
outcome includes release or deployment, reconstruct its next gate: MOS-3.7 if
review is missing, MOS-3.10 after verified merge if release is required, or
MOS-R.11 for the intended environment when its prerequisites are satisfied.
Compose the next safe output with its resolved kernel without another selector
or locator; QA PASS authorizes no merge, Release, or environment.

**Variables**
- Required: QA_RESULT
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Derived metadata:** the related issue or unit, the PR, the branch, and the
remaining verifiable relations are reconstructed from `QA_RESULT` and shown
resolved in the output for the receiver to verify; they are not manual inputs
nor fields the PM copies from GitHub, and they are never invented. Only real
material ambiguity —several incompatible sources equally active, or an
unverifiable relation— returns `status.needs_context` or
`status.needs_pm_decision`; a reconstructible identifier the PM did not retype
never fails closed.

**Deliver:** output.status_result (+output.route_prompt, output.pm_command_bundle). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-4.1. Next: MOS-3.5 for blocking-correction, MOS-3.3 for follow-up, MOS-3.7 if review is missing, MOS-3.10 if release applies after merge, or MOS-R.11 for the pending environment. MOS-4.8/MOS-4.7 retain compatible QA entry points. Recommended: the same unit's next safe output.
