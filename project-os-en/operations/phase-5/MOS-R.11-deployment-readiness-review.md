# MOS-R.11 — Deployment readiness review

MOSDLC operation `deployment-readiness-review` · Phase 5 — Local, staging, and production deployment · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.target_adoption, evidence.source_basis, evidence.validation_output, evidence.exact_ref
- PM approval: No (read-only readiness review)

**Does:** Check deployment readiness for a `TARGET_ENVIRONMENT`.
**For:** To unify local analysis/staging/production without deleting PM-facing operations per environment.
**How:** Apply the common continuity and evidence reuse contract to the
reconstructed unit and intended environment. Verify exact ref, applicable
validation, current QA/dispositions, and target prerequisites (including
merge/release or a previous environment only when required). Read adoption and
`Project-specific notes` live: configuration by safe names, deploy commands/
paths, tested rollback when mandatory, and that environment's post-deploy
checks. Identify responsible party and authorization for each action, without
treating prior success as readiness or permission for the next.

State reused, renewed, and missing evidence with source/ref/environment and
reason; readiness suffices only when all required checks are covered. If human
steps are missing, consume MOS-5.2, MOS-5.5, or MOS-5.8 to draft only pending
checks in the same response, retaining valid results. If satisfied, consume
MOS-R.12 under its resolved workflow and deliver the draft without another
mechanical checklist, selector, or locator. Execution approval remains a
separate gate; do not run the bundle.

Missing ref, validation, commands, environment evidence, or mandatory rollback
prevents claiming readiness and delivering execution commands. Invent no paths
and expand no authority to resolve configuration; identify the precise gap and
next safe action.

**Variables**
- Required: TARGET_REPOSITORY, TARGET_ENVIRONMENT
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. For missing evidence, nonexistent environment or PM decision required, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: QA/release or prior environment verification when required by the target; MOS-5.1/5.4/5.7 delegate this review. Next: MOS-R.12 if ready; environment checklist only for pending human checks. Recommended: deliver the next safe output in the same response.
