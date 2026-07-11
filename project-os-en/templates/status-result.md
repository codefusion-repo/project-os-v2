# Status result

Responsibility: return an unresolved status without padding it with repeated
rules.

```markdown
## Status

{{status.needs_context | status.needs_pm_decision | status.blocked}}

## Missing item, conflict, or blocker

{{What exactly is missing or blocked.}}

## Required source or decision

{{Where it should come from or who decides.}}

## Safe next step

{{Minimum step that preserves limits.}}
```
