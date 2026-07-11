# MOS-0.5 — Verify target adoption

MOSDLC operation `verify-target-adoption` · Phase 0 — Adoption · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.target_adoption · mode.review_only · output.status_result
- Evidence: evidence.target_adoption
- PM approval: No (read-only)

**Does:** Read-only audits that the target adoption exists, is correct and points to the current kernel.
**For:** Confirm that the target can operate safely.
**How:** Read adapters and target evidence without writing anything.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-0.2, MOS-0.3 or MOS-0.4. Next: MOS-1.1 or MOS-1.10 depending on the project. Recommended: MOS-R.2.
