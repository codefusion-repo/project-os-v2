# MOS-R.4 — Review phase readiness

MOSDLC operation `review-phase-readiness` · Cross-phase · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (advisory review; does not change phase)

**Does:** Review readiness advisory before moving work between MOSDLC phases.
**For:** To identify evidence, blockers and missing decisions before moving forward.
**How:** Contrast current phase, target phase and live state without executing transition.

**Variables**
- Required: — (none)
- Optional: TARGET_PHASE, READINESS_SOURCE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Derived metadata:** the current phase, the repository, the issue, the PR, and
the roadmap are derived metadata. `TARGET_PHASE` stays an input because it is a
human decision: it declares which phase the PM wants the work moved to, and
live evidence cannot substitute for it. `READINESS_SOURCE` is the single
primary locator and is asked for only when the current invocation does not
already identify the source; from it the current phase and the verifiable
relations are reconstructed.

**Deliver:** output.status_result. If there is evidence of a missing phase or ambiguous transition, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: closure or review of a phase. Next: safe operation of the target phase; MOS-R.3 if PM decision is missing; MOS-R.2 if routing is missing. Recommended: Safe operation of the target phase when ready.
