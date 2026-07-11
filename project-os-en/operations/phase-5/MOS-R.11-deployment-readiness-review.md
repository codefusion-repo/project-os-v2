# MOS-R.11 — Deployment readiness review

MOSDLC operation `deployment-readiness-review` · Phase 5 — Local, staging, and production deployment · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- PM approval: No (read-only readiness review)

**Does:** Check deployment readiness for a `TARGET_ENVIRONMENT`.
**For:** To unify local analysis/staging/production without deleting PM-facing operations per environment.
**How:** Verify configuration, target-owned commands, pending checklist and environment blockers.

**Variables**
- Required: TARGET_REPOSITORY, TARGET_ENVIRONMENT
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. For missing evidence, nonexistent environment or PM decision required, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-5.1, MOS-5.4 or MOS-5.7. Next: MOS-R.12 if there is readiness; If not, checklist of the corresponding environment. Recommended: MOS-R.12 when readiness is sufficient.
