# MOS-3.8 — Draft issue from description

MOSDLC operation `draft-issue-from-description` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only; the Human PM decides and runs the bundle)

**Does:** Draft a new issue from PM description while checking roadmap and documentation impact.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Turn DESCRIPTION into one scoped issue draft with source basis, scope, out-of-scope, acceptance criteria, validation, risk, and rollback.

**Variables**
- Required: DESCRIPTION
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.pm_command_bundle. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-1.7. Next: MOS-3.4. Recommended: MOS-3.4.
