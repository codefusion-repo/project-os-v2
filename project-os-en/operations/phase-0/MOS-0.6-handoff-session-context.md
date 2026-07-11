# MOS-0.6 — Handoff session context

MOSDLC operation `handoff-session-context` · Phase 0 — Adoption · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.handoff · mode.review_only · output.handoff_packet
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Packages live context and PM decisions to transfer to a new session.
**For:** Continue work without losing traceability.
**How:** Draft a rebuildable handoff packet from GitHub.

**Variables**
- Required: — (none)
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.handoff_packet. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: any phase. Next: MOS-0.1 in the new session. Recommended: MOS-0.1 in the new session.
