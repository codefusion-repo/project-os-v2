# MOS-3.3 — Draft follow up issue

MOSDLC operation `draft-follow-up-issue` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only; the Human PM decides and runs the bundle)

**Does:** Draft a follow-up issue from an incomplete issue.
**For:** Don't lose pending work when an issue closes incomplete.
**How:** Isolate what is missing in a follow-up with its own scope.

**Variables**
- Required: ISSUE_NUMBER
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.pm_command_bundle. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.13 or MOS-3.31. Next: MOS-3.4. Recommended: MOS-3.4.
