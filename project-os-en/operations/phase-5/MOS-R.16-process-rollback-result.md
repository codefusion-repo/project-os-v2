# MOS-R.16 — Process rollback result

MOSDLC operation `process-rollback-result` · Phase 5 — Local, staging, and production deployment · Risk: high.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (classification only; incidents and corrections have their own gates)

**Does:** Process an executed rollback result into an incident, correction, or closure path.
**For:** To close the deployment incident with traceability and post-rollback evidence.
**How:** Classify ROLLBACK_RESULT as restored, partial, or failed only when the evidence supports that result.

**Variables**
- Required: ROLLBACK_RESULT, TARGET_ENVIRONMENT
- Optional: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Return `status.blocked` if the environment remains unsafe.
- Do not redeploy, repeat rollback, run corrections, or authorize environment actions.
- Redact sensitive output and report only the command, check, and risk.

**Deliver:** output.status_result (+drafts if applicable). In case of unreadable evidence or next route with pending decision, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: PM run of MOS-R.15. Next: MOS-R.8 if there is an incident; MOS-3.3 for follow-ups. Recommended: MOS-R.8 when rollback exposes incident.
