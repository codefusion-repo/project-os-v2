# MOS-R.3 — PRocess needs pm decision

MOSDLC operation `process-needs-pm-decision` · Cross-phase — Accepted recommended operations · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle, output.draft_issue)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (classifies the decision; does not execute or self-approve)

**Does:** Process a status.needs_pm_decision result from any operation into exactly one safe decision outcome, without auto-approving, executing routes, or crossing the source operation's boundary.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Classify the pending PM decision into exactly one safe decision category:

**Variables**
- Required: DECISION_SOURCE, DECISION_CONTEXT, DECISION_QUESTION, DECISION_OPTIONS
- Optional: OPTIONS_IMPACT, PM_DECISION, PM_CLARIFICATION, ISSUE_NUMBER, PR_NUMBER, TARGET_REPOSITORY, ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- `PM_DECISION` decides only the explicit point; it never authorizes writes, future routes, or mutations.
- `PM_CLARIFICATION` and `PM_QUESTION_HUMANO` may narrow the question but never replace required evidence.
- If evidence contains secrets or secret-looking values, fail closed to `status.blocked` and request a redacted source basis.
- Do not execute routes, edit files or GitHub, or cross the source operation's limits.

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: none. Next: MOS-3.5, MOS-3.3, MOS-R.2. Recommended: none.
