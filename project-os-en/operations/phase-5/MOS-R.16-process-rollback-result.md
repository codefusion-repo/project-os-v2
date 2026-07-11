# MOS-R.16 — PRocess rollback result

MOSDLC operation `process-rollback-result` · Phase 5 — Local, staging, and production deployment · Risk: high.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (classification only; incidents and corrections have their own gates)

**Does:** Process the result of an executed rollback into incident, correction, or closure routes, draft-only, preserving traceability.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Classify ROLLBACK_RESULT as restored (safe state confirmed), partially restored, or failed only when evidence supports that route.

**Variables**
- Required: ROLLBACK_RESULT, TARGET_ENVIRONMENT
- Optional: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Return `status.blocked` if the environment remains unsafe.
- Do not redeploy, repeat rollback, run corrections, or authorize environment actions.
- Redact sensitive output and report only the command, check, and risk.

**Deliver:** output.status_result (+drafts when applicable). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.15. Next: MOS-R.8, MOS-3.3. Recommended: MOS-R.8.
