# MOS-3.26 — Process discipline audit

MOSDLC operation `process-discipline-audit` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Process the audit of discipline gaps and classify each finding.
**For:** To close the loop of the discipline audit.
**How:** Route blockers to correction and deferrables to follow-up.

**Variables**
- Required: AUDIT_RESULT
- Optional: ISSUE_NUMBER, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result (+output.route_prompt, output.pm_command_bundle). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.24. Next: MOS-3.5 or MOS-3.3. Recommended: MOS-3.3.
