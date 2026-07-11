# MOS-4.5 — PRocess qa checklist feature

MOSDLC operation `process-qa-checklist-feature` · Phase 4 — QA and human verification · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Classify human QA checklist results for a described feature into issue creation, correction, follow-up, no-op, implementation, or PM decision paths.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Classify QA_RESULT findings as blocking correction, non-blocking follow-up, new issue, no-op, implementation, or PM decision only when evidence supports that route.

**Variables**
- Required: QA_RESULT
- Optional: DESCRIPTION, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result (+output.route_prompt, output.pm_command_bundle). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-4.2. Next: MOS-3.8, MOS-4.7. Recommended: MOS-3.8.
