# MOS-R.3 — Process a pending PM decision

MOSDLC operation `process-needs-pm-decision` · Cross-phase · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle, output.draft_issue)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (classifies the decision; does not execute or self-approve)

**Does:** Reconstruct a pending PM decision from live evidence and process it into a safe output.
**For:** To resolve pending PM decisions with clear and target-agnostic variables.
**How:** Read the typed issue or PR, reconstruct the pending point from `DECISION_SOURCE`, and either validate a decision already made or present options with impact, tradeoffs, a recommendation, and the exact question.

**Variables**
- Required: ISSUE_OR_PR, DECISION_SOURCE, PM_DECISION_ALREADY_MADE
- Optional: DECISION_OPTIONS, PM_DECISION

**Safeguards**
- `ISSUE_OR_PR` accepts exactly one typed `issue #N` or `PR #N` reference; resolve the repository from active adoption and return `status.needs_context` when it is not unambiguous.
- `PM_DECISION_ALREADY_MADE` is `true` or `false`: when `true`, `PM_DECISION` is required; when `false`, it must be empty.
- If `PM_DECISION_ALREADY_MADE=false`, use `DECISION_OPTIONS` when supplied or derive a bounded set from live evidence; deliver impact, tradeoffs, risks, reversibility, a recommendation, and the exact question.
- `PM_DECISION` decides only the explicit point; it never authorizes writes, implementation, merge, closure, tag, release, deploy, future routes, or other mutations.
- For an ambiguous decision, missing evidence, or a contradiction with durable evidence, fail closed with `status.needs_pm_decision` or `status.needs_context`, as appropriate.
- If evidence contains secrets or secret-looking values, fail closed to `status.blocked` and request a redacted source basis.
- Do not execute routes, edit files or GitHub, or cross the source operation's limits.

**Deliver:** output.status_result, with route prompt only for limited correction and draft issue/bundle only for follow-up. When a decision already made is sufficient, return to the source operation; when options are needed, present the recommendation without executing or self-approving any option.

**Connections:** Previous: any operation with `status.needs_pm_decision`. Next: return to DECISION_SOURCE if sufficient; MOS-3.5 for correction; MOS-3.3 for follow-up; MOS-R.2 if only routing is missing. Recommended: Return to DECISION_SOURCE when safe.
