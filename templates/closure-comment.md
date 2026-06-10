# Closure comment template

The closure comment is the reconstruction packet for the next agent (which may
be a different AI tool). Post it on the issue before or at closing time.

```markdown
## Completion evidence

- [What now exists: behavior, files, decisions. Reference the merged PR.]

## Validation evidence

- [Each validation command with its real result, e.g. `pytest -q`: 15 passed.]

## Boundaries preserved

- [What was deliberately NOT done or changed — this tells the next agent what
  not to assume exists.]

## References

- PR #[n] (merged), commits on `work/<issue>-<slug>`.
- Follow-ups filed: #[n], #[n] (or "none").

## Friction note

[One line: what slowed this down or felt unnecessary. Used to tune the process.]
```
