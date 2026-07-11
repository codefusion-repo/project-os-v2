# MOS-4.7 — Draft a follow-up from QA

MOSDLC operation `draft-follow-up-from-qa` · Phase 4 — QA and human verification · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only; the Human PM decides and runs the bundle)

**Does:** Draft follow-up from QA results.
**For:** Defer non-blocking QA findings with traceability.
**How:** Follow-up creation bundle for the Human PM.

**Variables**
- Required: QA_RESULT
- Optional: ISSUE_NUMBER, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.pm_command_bundle. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-4.4, MOS-4.5 or MOS-4.6. Next: MOS-3.4 when prioritized. Recommended: MOS-3.4.
