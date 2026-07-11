# MOS-R.9 — Audit docs product drift

MOSDLC operation `audit-docs-product-drift` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.source_basis
- PM approval: No (read-only audit)

**Does:** Audit drift between documentation and real product.
**For:** Maintain docs as usable truth of the product.
**How:** Contrast docs, code and live status; Actionable drift list with evidence.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. Given unreadable docs, code or live status, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.27 or status review. Next: MOS-1.8 if the drift is documentary; MOS-3.3 for product follow-ups. Recommended: MOS-1.8 when the drift is documentary.
