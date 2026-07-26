# MOS-4.8 — Draft a correction from QA

MOSDLC operation `draft-correction-from-qa` · Phase 4 — QA and human verification · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (the route prompt does not authorize; writing requires exact PM approval)

**Does:** Draft the correction prompt from QA results.
**For:** To fix QA blockers without expanding the scope.
**How:** Encapsulate QA_RESULT in a delegated correction path.

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

**Deliver:** output.route_prompt. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-4.4. Next: MOS-3.7. Recommended: MOS-3.7.
