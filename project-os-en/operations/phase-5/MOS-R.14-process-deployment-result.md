# MOS-R.14 — PRocess deployment result

MOSDLC operation `process-deployment-result` · Phase 5 — Local, staging, and production deployment · Risk: high.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (classification only; rollback and correction have their own gates)

**Does:** Process a deployment result (success, partial, or failure) into a safe continue, correct, or rollback route, draft-only.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Classify DEPLOYMENT_RESULT as continue (healthy), scoped correction, or rollback candidate only when evidence supports that route.

**Variables**
- Required: DEPLOYMENT_RESULT, TARGET_ENVIRONMENT
- Optional: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Rollback is never automatic; the PM decides and MOS-R.15 drafts it.
- Route prompts and bundles are non-authorizing or PM-executed; do not run environment actions.
- Redact sensitive values as `[REDACTED]` and report only command/check names and risk types.

**Deliver:** output.status_result (+drafts when applicable). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.13. Next: MOS-R.15, MOS-3.3. Recommended: MOS-R.15.
