# MOS-R.14 — Process deployment result

MOSDLC operation `process-deployment-result` · Phase 5 — Local, staging, and production deployment · Risk: high.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (classification only; rollback and correction have their own gates)

**Does:** Process a successful, partial, or failed deployment into a continue, fix, or rollback path.
**For:** To decide next path with evidence, not unverified deploy output.
**How:** Compare DEPLOYMENT_RESULT with MOS-R.13 evidence for the same unit,
target, ref, and environment. Verified success allows reconstructing readiness
for the pending intended environment through MOS-R.11, renewing its specific
evidence and showing its exact gate; it does not imply promotion. On failure,
retain the unit, classify correction through the applicable route or PM rollback
decision through MOS-R.15; follow-up requires MOS-3.3 materiality and independence.
Deliver the safe output in the same response and redact any sensitive data.

**Variables**
- Required: DEPLOYMENT_RESULT, TARGET_ENVIRONMENT
- Optional: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Rollback is never automatic; the PM decides and MOS-R.15 drafts it.
- Route prompts and bundles are non-authorizing or PM-executed; do not run environment actions.
- Redact sensitive values as `[REDACTED]` and report only command/check names and risk types.

**Deliver:** output.status_result (+drafts if applicable). If the result or verification is unreadable, or the continue/rollback election is pending, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.13. Next: MOS-R.11 for a pending environment with verified success; MOS-R.15 if PM chooses rollback; unit correction or MOS-3.3 only for an independent outcome. Recommended: the same unit's next safe action, without automatic promotion.
