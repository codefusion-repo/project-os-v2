# Issue template

One issue per outcome. Body under ~5KB. If "Why this exists" cannot be written
in three sentences, the issue should not exist.

The issue is the execution source of detail: route prompts stay compact, so
the issue must carry enough objective, source basis, scope, out-of-scope,
acceptance criteria, validation commands, risk, and rollback for a terminal
agent to execute after reading the issue body live.

~~~markdown
## Why this exists

[1-3 sentences: the real problem this reduces.]

## Objective

[The observable result when this closes.]

## Source basis

- [Links to the roadmap item, prior issues/PRs, ADRs, or decisions this builds on.]

## Scope

- [Max ~5 bullets. Files/areas/behavior included.]

## Out of scope

- [Only things an agent might plausibly attempt. Max ~5 bullets.]

## Decisions included

[Design micro-decisions are made here, not in separate review issues. Omit if none.]

## Acceptance criteria

- [Observable criteria.]

## Validation

- [Exact commands and expected results.]

## Risk and rollback

[1-2 sentences. "Revert the PR" is a valid rollback.]
~~~
