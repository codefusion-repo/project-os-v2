# MOS-0.5 — Verify target adoption

MOSDLC operation `verify-target-adoption` · Phase 0 — Adoption · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.target_adoption · mode.review_only · output.status_result
- Evidence: evidence.target_adoption
- PM approval: No (read-only)

**Does:** Audit read-only whether a target repository adoption exists, is correct, and points to the current kernel standard.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Report present, missing, stale, drifted, or unsafe adoption elements.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-0.2, MOS-0.3, MOS-0.4. Next: MOS-1.1, MOS-1.10. Recommended: MOS-R.2.
