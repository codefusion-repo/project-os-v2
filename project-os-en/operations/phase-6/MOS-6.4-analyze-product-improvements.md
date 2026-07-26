# MOS-6.4 — Analyze product improvements

MOSDLC operation `analyze-product-improvements` · Phase 6 — Maintenance and improvements · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.review_result (+output.status_result)
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Analyze and recommend product improvements.
**For:** To inform the roadmap with evidence-based improvements.
**How:** Read-only analysis of the product against usage and docs, delivered as
findings with their reference, verifiable disposition, recommendation, risks,
and what was not reviewed.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.review_result (+output.status_result). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: periodic maintenance. Next: MOS-6.10. Recommended: MOS-6.10.
