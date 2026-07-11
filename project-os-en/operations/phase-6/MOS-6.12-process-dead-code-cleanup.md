# MOS-6.12 — Process dead code cleanup

MOSDLC operation `process-dead-code-cleanup` · Phase 6 — Maintenance and improvements · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Processes cleanup of detected useless code.
**For:** Carry out the cleaning with a limited and safe scope.
**How:** Draft the delegated cleaning route in limited batches.

**Variables**
- Required: AUDIT_RESULT
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result (+output.route_prompt, output.pm_command_bundle). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-6.6. Next: MOS-3.8 or MOS-3.3. Recommended: MOS-3.8.
