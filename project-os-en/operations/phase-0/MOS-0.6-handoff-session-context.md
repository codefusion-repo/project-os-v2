# MOS-0.6 — Handoff session context

MOSDLC operation `handoff-session-context` · Phase 0 — Adoption · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.handoff · mode.review_only · output.handoff_packet
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Draft a handoff packet that lets a new session reconstruct context from live evidence.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft a compact handoff packet with what was verified, what remains assumed, open PM decisions, active boundaries, and next operation.

**Variables**
- Required: — (none)
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.handoff_packet. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: none. Next: MOS-0.1. Recommended: MOS-0.1.
