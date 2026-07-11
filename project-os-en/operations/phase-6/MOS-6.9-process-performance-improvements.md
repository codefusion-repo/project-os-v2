# MOS-6.9 — PRocess performance improvements

MOSDLC operation `process-performance-improvements` · Phase 6 — Production readiness and maintenance · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Process recommended performance improvements into prioritized work.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Classify AUDIT_RESULT performance recommendations as new implementation work, non-blocking follow-up, or PM decision only when evidence supports that route.

**Variables**
- Required: AUDIT_RESULT
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result (+output.route_prompt, output.pm_command_bundle). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-6.3. Next: MOS-3.8, MOS-3.3. Recommended: MOS-3.3.
