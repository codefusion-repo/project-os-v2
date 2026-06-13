# Closure comment template

The closure comment is the reconstruction packet for the next agent (which may
be a different AI tool). Post it on the issue before or at closing time.

~~~markdown
## Completion evidence

- [What now exists: behavior, files, decisions. Reference the merged PR.]

## Validation evidence

- [Each validation command with its real result, e.g. `pytest -q`: 15 passed.]

## Accepted exceptions

- [None, or a scoped PM-accepted validation/CI exception. If present, state
  what failed, why it is accepted, what tracks it if needed, and why it does not
  block this closure.]

## Boundaries preserved

- [What was deliberately NOT done or changed — this tells the next agent what
  not to assume exists.]

## Friction note

[Required, one concise line: what slowed this down or felt unnecessary. If no
friction was observed, say so.]

## References

- PR #[n] (merged), commits on `work/<issue>-<slug>`.
- Follow-ups filed: #[n], #[n] (or "none").
~~~
