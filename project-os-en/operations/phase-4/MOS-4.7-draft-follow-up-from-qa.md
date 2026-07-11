# MOS-4.7 — Draft follow up from qa

MOSDLC operation `draft-follow-up-from-qa` · Phase 4 — QA and human verification · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only; the Human PM decides and runs the bundle)

**Does:** Draft a Human PM-executed follow-up issue bundle from non-blocking QA findings.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Extract non-blocking QA findings from QA_RESULT into one focused follow-up issue draft or a small bounded bundle when evidence requires separation.

**Variables**
- Required: QA_RESULT
- Optional: ISSUE_NUMBER, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.pm_command_bundle. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-4.4, MOS-4.5, MOS-4.6. Next: MOS-3.4. Recommended: MOS-3.4.
