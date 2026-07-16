# Status result

Responsibility: return a status and, when MOS-R.3 processes a PM decision,
its canonical resolution without padding it with repeated rules.

```markdown
## Status

{{status.resolved | status.needs_context | status.needs_pm_decision | status.blocked}}

## PM decision resolution (only when applicable)

- decision_key: {{project/target · work unit · material action · exact scope}}
- superseded_decision: {{unique most recent earlier exact, sufficient decision; none if tied}}
- current_pm_decision: {{current decision or none}}
- required_traceability_follow_up: {{durable drift to reconcile or none}}
- remaining_gates: {{independent gates and their status}}
- resulting_status: {{selected status}}
- safe_return_operation: {{safe source operation}}

## Missing item, conflict, or blocker

{{What exactly is missing or blocked.}}

## Required source or decision

{{Where it should come from or who decides.}}

## Safe next step

{{Minimum step that preserves limits.}}
```
