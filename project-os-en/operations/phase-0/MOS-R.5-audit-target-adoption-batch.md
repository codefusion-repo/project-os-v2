# MOS-R.5 — Audit target adoption batch

MOSDLC operation `audit-target-adoption-batch` · Phase 0 — Adoption · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.target_adoption
- PM approval: No (read-only audit)

**Does:** Audit the adoption of several target repositories in a single pass.
**For:** To maintain multiple adopted targets without accumulated drift.
**How:** Verify adoption for each target and consolidate drift, missing adapters, and stale adoption.

**Variables**
- Required: TARGET_REPOSITORIES
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If there is an empty list, an unreadable target or missing adoption evidence, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-0.5 or adoption maintenance. Next: MOS-0.4 per target with drift. Recommended: MOS-0.4 per target with drift.
