# MOS-6.7 — PRocess security production results

MOSDLC operation `process-security-production-results` · Phase 6 — Production readiness and maintenance · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Process security-for-production-readiness results into blocking or deferrable actions.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Classify SECURITY_REVIEW_RESULT findings as blocking correction, non-blocking follow-up, or PM decision only when evidence supports that route.

**Variables**
- Required: SECURITY_REVIEW_RESULT
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Strict security posture: describe sensitive surfaces only by variable name, command, path, or risk type; never expose secrets, `.env` values, tokens, or credentials.

**Deliver:** output.status_result (+output.route_prompt, output.pm_command_bundle). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-6.1. Next: MOS-3.5, MOS-3.3. Recommended: MOS-3.5.
