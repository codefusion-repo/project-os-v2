# MOS-6.3 — Analyze performance improvements

MOSDLC operation `analyze-performance-improvements` · Phase 6 — Maintenance and improvements · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Analyze and recommend performance improvements.
**For:** To prioritize optimizations with evidence.
**How:** Read-only analysis with actionable recommendations.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PATH_SCOPE, FOCUS, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: periodic maintenance. Next: MOS-6.9. Recommended: MOS-6.9.
