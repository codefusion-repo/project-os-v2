# MOS-R.5 — Audit target adoption batch

MOSDLC operation `audit-target-adoption-batch` · Phase 0 — Adoption · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.target_adoption
- PM approval: No (read-only audit)

**Does:** Audit the adoption of multiple target projects in one batch, read-only, and consolidate drift per target.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Read-only iteration of the single-target adoption verification over every repository in TARGET_REPOSITORIES, consolidating per-target drift, missing adapters, and stale kernel adoption.

**Variables**
- Required: TARGET_REPOSITORIES
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-0.5. Next: MOS-0.4. Recommended: MOS-0.4.
