# Artifact templates

Fill-in shapes for the GitHub artifacts agents produce. Copy the relevant block,
fill it, and post it. Shape only — a template never grants permission.

Sections: [Issue](#issue) · [Pull request](#pull-request) ·
[Closure comment](#closure-comment) · [ADR](#adr) · [Roadmap issue](#roadmap-issue).

## Issue

One issue per outcome. Body under ~5KB. If "Why this exists" cannot be written in
three sentences, the issue should not exist. The issue is the execution source of
detail: route prompts stay compact, so the issue must carry enough objective,
source basis, scope, out-of-scope, acceptance criteria, validation, risk, and
rollback for a terminal agent to execute after reading the issue body live.

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

## Pull request

~~~markdown
## Summary

- [What this PR does, in terms of behavior.]

## Scope / Boundaries

- [What surfaces/areas it touches and deliberately does not touch.]
- Merge and issue closure are not requested by this PR.

## Validation

- `[command]` — [result]
- `[command]` — [result]

## Security / Privacy

- [Sensitive data handling, or "no sensitive surfaces touched".]

Closes #[issue] (on PM merge decision).
~~~

## Closure comment

The reconstruction packet for the next agent (which may be a different AI tool).
Post it on the issue before or at closing time.

~~~markdown
## Completion evidence

- [What now exists: behavior, files, decisions. Reference the merged PR.]

## Validation evidence

- [Each validation command with its real result, e.g. `pytest -q`: 15 passed.]

## Accepted exceptions

- [None, or a scoped PM-accepted validation/CI exception. If present, state what
  failed, why it is accepted, what tracks it if needed, and why it does not block
  this closure.]

## Boundaries preserved

- [What was deliberately NOT done or changed — this tells the next agent what not
  to assume exists.]

## Friction note

[Required, one concise line: what slowed this down or felt unnecessary. If no
friction was observed, say so.]

## References

- PR #[n] (merged), commits on `work/<issue>-<slug>`.
- Follow-ups filed: #[n], #[n] (or "none").
~~~

## ADR

For decisions that outlive issues. Store as `docs/decisions/ADR-NNNN-<slug>.md`
in the project that owns the decision.

~~~markdown
# ADR-NNNN: [Title]

- Status: accepted | superseded by ADR-NNNN
- Date: [YYYY-MM-DD]

## Context

[The forces and evidence that made this decision necessary.]

## Decision

[What was decided, stated as a rule future work can follow.]

## Consequences

[What this enables, what it forbids, and the accepted tradeoffs.]
~~~

## Roadmap issue

One canonical roadmap issue per project. It answers "what comes next and why". It
supersedes; it does not store mutable status (issue/PR state stays live).

**Normalization path** — when normalizing an existing roadmap, choose from live
GitHub evidence and exact PM approval for that repository and action:

- Edit the existing roadmap in place when adapters, reference issues, closure
  comments, PRs, or active work hard-code its issue number and changing it would
  create ambiguity.
- Create a new superseding roadmap issue when the old one is better preserved as
  history, references are not coupled to its number, or a clean authority is safer.
- Either way, preserve prior decisions, constraints, unresolved objectives, and
  deferred work (edit history, a normalization comment, carried-forward issues, or
  supersession links), and record the rationale in comments.
- Do not store live state in durable files. Neither path authorizes
  implementation, closure, labels, releases, settings, automation, or target
  mutations; each write needs its own evidence and exact PM approval.

~~~markdown
## Purpose

[What this roadmap takes the project from and to. 2-4 sentences.]

## Phases

### [PHASE-ID] — [Name]

[Objective in 1-2 sentences.]

Exit criteria:
- [Observable, evidence-based criteria.]

[Repeat per phase. Prefer 3-5 phases over 15.]

## Kill criteria

- [Conditions under which this direction is abandoned, decided in advance.]

## Not now / out of scope

- [What is deliberately deferred until evidence justifies it.]

## Non-authorization

This roadmap authorizes no writes by itself; every write-capable action needs its
own scoped approval.
~~~
