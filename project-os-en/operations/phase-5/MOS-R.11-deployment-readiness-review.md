# MOS-R.11 — Deployment readiness review

MOSDLC operation `deployment-readiness-review` · Phase 5 — Local, staging, and production deployment · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- PM approval: No (read-only readiness review)

**Does:** Review deployment readiness for one environment selected by TARGET_ENVIRONMENT, read-only and parameterized.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Read-only readiness review for TARGET_ENVIRONMENT: configuration presence, target-owned deploy commands, pending checklist items, and unresolved blockers, without collapsing the per-environment PM-facing operations.

**Variables**
- Required: TARGET_REPOSITORY, TARGET_ENVIRONMENT
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-5.1, MOS-5.4, MOS-5.7. Next: MOS-R.12. Recommended: MOS-R.12.
