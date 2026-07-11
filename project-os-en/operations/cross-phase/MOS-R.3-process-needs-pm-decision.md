# MOS-R.3 — Process a pending PM decision

MOSDLC operation `process-needs-pm-decision` · Cross-phase · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle, output.draft_issue)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (classifies the decision; does not execute or self-approve)

**Does:** Process a `status.needs_pm_decision` from a source operation into a safe output.
**For:** Resolve pending PM decisions with clear and target-agnostic variables.
**How:** Classify the decision as missing context, route selection, correction approval, follow-up creation, stop/no-op, return to the source, or a request for more evidence.

**Variables**
- Required: DECISION_SOURCE, DECISION_CONTEXT, DECISION_QUESTION, DECISION_OPTIONS
- Optional: OPTIONS_IMPACT, PM_DECISION, PM_CLARIFICATION, ISSUE_NUMBER, PR_NUMBER, TARGET_REPOSITORY, ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- `PM_DECISION` decides only the explicit point; it never authorizes writes, future routes, or mutations.
- `PM_CLARIFICATION` and `PM_QUESTION_HUMANO` may narrow the question but never replace required evidence.
- If evidence contains secrets or secret-looking values, fail closed to `status.blocked` and request a redacted source basis.
- Do not execute routes, edit files or GitHub, or cross the source operation's limits.

**Deliver:** output.status_result, with route prompt only for limited correction and draft issue/bundle only for follow-up. In case of ambiguous evidence, scope or decision, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: any operation with `status.needs_pm_decision`. Next: return to DECISION_SOURCE if sufficient; MOS-3.5 for correction; MOS-3.3 for follow-up; MOS-R.2 if only routing is missing. Recommended: Return to DECISION_SOURCE when safe.
