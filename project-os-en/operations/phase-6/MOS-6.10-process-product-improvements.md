# MOS-6.10 — PRocess product improvements

MOSDLC operation `process-product-improvements` · Phase 6 — Production readiness and maintenance · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Process recommended product improvements into roadmap, backlog, or PM decisions.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Classify AUDIT_RESULT product recommendations as roadmap-affecting, new implementation work, non-blocking follow-up, or no-op only when evidence supports that route.

**Variables**
- Required: AUDIT_RESULT
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result (+output.route_prompt, output.pm_command_bundle). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-6.4. Next: MOS-1.8, MOS-3.8. Recommended: MOS-1.8.
