# MOS-3.14 — PRocess traceability audit

MOSDLC operation `process-traceability-audit` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Classify traceability audit findings into correction, follow-up, no-op, or PM decision paths.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Classify AUDIT_RESULT findings into blocking correction, non-blocking follow-up, no-op, or PM decision.

**Variables**
- Required: AUDIT_RESULT
- Optional: ISSUE_NUMBER, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result (+output.route_prompt, output.pm_command_bundle). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.13. Next: MOS-3.5, MOS-3.3. Recommended: MOS-3.3.
