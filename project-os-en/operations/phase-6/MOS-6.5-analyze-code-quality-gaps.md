# MOS-6.5 — Analyze code quality gaps

MOSDLC operation `analyze-code-quality-gaps` · Phase 6 — Production readiness and maintenance · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Analyze and recommend code normalization improvements or clean-code gaps.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Inspect codebase structure and selected files for evidence-backed normalization and clean-code gaps.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PATH_SCOPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: none. Next: MOS-6.11. Recommended: MOS-6.11.
