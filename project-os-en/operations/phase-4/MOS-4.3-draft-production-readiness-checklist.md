# MOS-4.3 — Draft production readiness checklist

MOSDLC operation `draft-production-readiness-checklist` · Phase 4 — QA and human verification · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Draft the human QA checklist for production readiness.
**For:** To verify actual preparation before considering production.
**How:** Cross-sectional readiness checklist verifiable by a human. Apply the
common continuity contract to the unit, criteria, ref, and intended environment;
retain current human checks and distinguish pending or affected ones. The QA
result feeds MOS-4.6; it replaces neither environment-specific MOS-R.11 readiness
nor production approval.

**Variables**
- Required: — (none)
- Optional: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.4. Next: MOS-4.6. Recommended: MOS-4.6.
