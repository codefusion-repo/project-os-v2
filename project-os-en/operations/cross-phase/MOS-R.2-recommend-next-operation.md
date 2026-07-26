# MOS-R.2 — Recommend next operation

MOSDLC operation `recommend-next-operation` · Cross-phase · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (recommendation only; does not execute or authorize)

**Does:** Recommend exactly one next MOSDLC operation from live traceability.
**For:** To choose lifecycle path without ad hoc reasoning.
**How:** Read live status, justify the recommendation and show safe alternatives if there is ambiguity.

**Variables**
- Required: — (none)
- Optional: ROUTING_SOURCE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Derived metadata:** the repository, the issue, the PR, the roadmap, and the
current status are derived metadata, not inputs. Apply the common contract's
precedence: reuse the unambiguous source the current invocation already
identifies; if none exists, ask for a single `ROUTING_SOURCE` —repository,
issue, PR, roadmap, or equivalent live record— and reconstruct the rest from
it. Return the decision to the PM only on real material ambiguity, never
because a reconstructible identifier is missing.

**Deliver:** output.status_result. In the event of insufficient or unreadable traceability, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: any operation that requires routing. Next: the recommended operation, invoked by the Human PM. Recommended: The recommended operation.
