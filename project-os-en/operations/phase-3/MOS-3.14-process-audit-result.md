# MOS-3.14 — Process audit result

MOSDLC operation `process-audit-result` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Process the result of any audit (traceability, discipline, or other)
and classify the safe route.
**For:** To convert audit findings into concrete actions without fragmenting the
processing by audit type.
**How:** Classify each finding with its verifiable disposition and route it to
correction (`blocking-correction` → MOS-3.5), follow-up (`non-blocking-follow-up`
→ MOS-3.3), or no-op (`preference`, `accepted-risk`, `invalid-finding`). The
source audit travels in `AUDIT_RESULT`; the operation does not depend on the
originating audit type.

**Variables**
- Required: AUDIT_RESULT
- Optional: ISSUE_NUMBER, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result (+output.route_prompt, output.pm_command_bundle). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.13, MOS-3.24, or another audit. Next: MOS-3.5 or MOS-3.3. Recommended: MOS-3.3 for non-blocking.
