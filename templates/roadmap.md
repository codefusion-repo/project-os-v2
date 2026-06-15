# Roadmap issue template

One canonical roadmap issue per project. It answers "what comes next and why".
It supersedes; it does not store mutable status (issue/PR state stays live).

## Roadmap normalization path

When normalizing an existing project roadmap, choose the path from live GitHub
evidence and exact PM approval for that repository and action.

- Edit the existing roadmap in place when current adapters, reference issues,
  closure comments, PRs, or active work hard-code that roadmap issue number and
  changing the number would create ambiguity or a transition window.
- Create a new superseding roadmap issue when the old issue is better preserved
  as historical context, references are not tightly coupled to its number, or a
  clean new authority is safer than rewriting the old body.
- In both paths, preserve old roadmap context: keep prior decisions, constraints,
  unresolved objectives, and deferred work either in the issue edit history, a
  context-preserving normalization comment, carried-forward issues, or explicit
  supersession links.
- Record the normalization rationale in comments. For in-place edits, rely on
  edit history plus a mapping comment that explains where the old structure
  moved. For superseding issues, comment on the old issue before closing or
  superseding it, with a pointer to the new roadmap and the preserved context.
- Do not store live state in durable files or roadmap bodies. Issue, PR, branch,
  validation, review, and release state remains in GitHub and git, read at task
  time.
- Neither path authorizes implementation, closure, labels, releases, settings,
  automation, or target mutations. Each write requires its own live evidence and
  exact PM approval.

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

This roadmap authorizes no writes by itself; every write-capable action needs
its own scoped approval.
~~~
