# MOS-4.7 — Draft a follow-up from QA

MOSDLC operation `draft-follow-up-from-qa` · Phase 4 — QA and human verification · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only; the Human PM decides and runs the bundle)

**Does:** Draft follow-up from QA results.
**For:** To defer non-blocking QA findings with traceability.
**How:** Use MOS-3.3 as the sole follow-up contract: `QA_RESULT` is its
already available `FOLLOW_UP_SOURCE`. Read and apply that contract in this same
response, including materiality, independence, grouping, unit reuse, and
no-action. Do not ask for another locator or turn each QA finding into an issue.
Keep this compatible entry point; it is neither a separate semantic contract
nor a mandatory handoff.

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

**Deliver:** output.pm_command_bundle. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-4.4, MOS-4.5 or MOS-4.6. Next: MOS-3.4 when prioritized. Recommended: MOS-3.4.
