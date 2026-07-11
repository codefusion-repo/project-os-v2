# MOS-0.1 — Activate browser session

MOSDLC operation `activate-browser-session` · Phase 0 — Adoption · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Establish the PM draft-only session in browser chat by resolving the kernel manifest.
**For:** To start any MOSDLC cycle with correct boundaries and context.
**How:** Resolve the kernel, read the minimum live state, and report the initial status.

**Variables**
- Required: — (none)
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: -. Next: MOS-0.2, MOS-0.3, MOS-0.5. Recommended: MOS-0.5 if there is a target adopted; MOS-0.2 or MOS-0.3 if not.
