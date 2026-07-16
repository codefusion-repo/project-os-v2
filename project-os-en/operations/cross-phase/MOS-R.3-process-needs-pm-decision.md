# MOS-R.3 — Process a pending PM decision

MOSDLC operation `process-needs-pm-decision` · Cross-phase · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle, output.draft_issue)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (classifies the decision; does not execute or self-approve)

**Does:** Process a pending PM decision from live evidence into a safe output.
**For:** To resolve pending PM decisions with clear and target-agnostic variables.
**How:** Read the issue and/or PR identified by their numbers, reconstruct the pending point from `DECISION_SOURCE`, and apply `rule.precedencia_decision_pm`: validate the current decision or present options with impact, tradeoffs, a recommendation, and the exact question.

**Variables**
- Required: DECISION_SOURCE, PM_DECISION_ALREADY_MADE
- Optional: ISSUE_NUMBER, PR_NUMBER, DECISION_OPTIONS, PM_DECISION

**Safeguards**
- `ISSUE_NUMBER` and `PR_NUMBER` are optional numeric references and, when supplied, accept positive numbers only. Both may remain blank: derive context from `DECISION_SOURCE` and live evidence, and return `status.needs_context` only when it cannot be derived unambiguously during execution.
- Both references may be supplied when they belong to a verifiably related flow; if they are unrelated, fail closed.
- `PM_DECISION_ALREADY_MADE` is `true` or `false`: when `true`, `PM_DECISION` is required; when `false`, it must be empty.
- If `PM_DECISION_ALREADY_MADE=false`, use `DECISION_OPTIONS` when supplied or derive a bounded set from live evidence; deliver impact, tradeoffs, risks, reversibility, a recommendation, and the exact question.
- Form a material `decision_key` with the project or target, work unit, material action, and exact scope. Verify source and chronological order as separate evidence for each decision; compare only decisions with the same material key. A Release approval does not authorize closure, settings, publication, transition, or another separate action.
- A later, explicit, exact, applicable decision from a verifiable live source becomes `current_pm_decision`; retain as `superseded_decision` only the most recent earlier decision that is also exact and sufficient. If multiple earlier exact, sufficient candidates tie at the greatest eligible chronological order, do not choose by input order: leave `superseded_decision` unresolved, retain the already resolved `current_pm_decision`, and return `status.needs_pm_decision`.
- For drift with earlier durable evidence, identify the contradictory source in `required_traceability_follow_up` without rewriting history. That drift alone does not block an action whose `remaining_gates` are satisfied.
- Always deliver `decision_key`, `superseded_decision`, `current_pm_decision`, `required_traceability_follow_up`, `remaining_gates`, `resulting_status`, and `safe_return_operation`.
- Retain `superseded_decision` and `current_pm_decision` when a current decision is already resolved even if an independent `remaining_gate` blocks. Use `status.resolved` only with an exact current decision, unambiguous supersession when applicable, supported output, and every other gate satisfied. Use `status.needs_pm_decision` when the current decision, material key, or selection of `superseded_decision` is ambiguous; `status.needs_context` when the source, provenance, order, or verifiable relationship is missing; and `status.blocked` for a mutation with unverifiable or insufficient exact approval, incompatible actor/mode/surface/permission, secrets, failed validation, a non-delegable limit, or extension to another action.
- `PM_DECISION` decides only the explicit point; it never authorizes writes, implementation, merge, closure, tag, release, deploy, future routes, or other mutations, and never relaxes non-delegable limits or separate approvals.
- If evidence contains secrets or secret-looking values, fail closed to `status.blocked` and request a redacted source basis.
- Do not execute routes, edit files or GitHub, or cross the source operation's limits.

**Deliver:** output.status_result in the canonical decision-resolution form; a route prompt only for limited correction and a draft issue/bundle only for traceability follow-up. When the current decision and gates are sufficient, return to the source operation; when options are needed, present the recommendation without executing or self-approving any option.

**Connections:** Previous: any operation with `status.needs_pm_decision`. Next: return to DECISION_SOURCE if sufficient; MOS-3.5 for correction; MOS-3.3 for follow-up; MOS-R.2 if only routing is missing. Recommended: Return to DECISION_SOURCE when safe.
