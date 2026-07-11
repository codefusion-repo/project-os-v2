# MOS-3.28 — Draft follow up from audit

MOSDLC operation `draft-follow-up-from-audit` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only; the Human PM decides and runs the bundle)

**Does:** Draft a follow-up issue from non-blocking implementation-discipline audit findings.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Extract deferred implementation-discipline findings from AUDIT_RESULT into one focused follow-up issue draft.

**Variables**
- Required: AUDIT_RESULT
- Optional: ISSUE_NUMBER, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.pm_command_bundle. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.26. Next: MOS-3.4. Recommended: MOS-3.4.
