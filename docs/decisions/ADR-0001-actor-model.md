# ADR-0001: The actor model is surface-only; reviewer/QA/asset/security are not actors

- Status: accepted
- Date: 2026-06-19

## Context

`kernel/actors.json` defines capability by **execution surface**
(`actor.human_pm`, `actor.terminal_agent`, `actor.browser_chat`,
`actor.unknown`), never by role. Earlier roadmap work listed four candidate
actors — reviewer, QA, asset creator, and security reviewer — and that
"candidate actor" language spread across the roadmap issue, an operations
catalog, and prompt comments. A cold human or AI agent could not tell whether
those actors exist. Adding role-actors would also reintroduce the role/actor
duplication the surface-based model was built to remove, and `docs/DESIGN.md`
requires a named, observed failure before any new kernel entry.

## Decision

The four surfaces in `kernel/actors.json` are the only actors. There are no
role-based actors. Reviewer, QA, asset creator, and security reviewer are
**not** actors; each is one of:

- a **review focus** — e.g. a security or QA review is `workflow.review_before_close`
  / `workflow.review_only` run on an existing surface, producing `output.review_result`;
- a **gate** — a QA or security verdict is evidence that can return
  `status.needs_pm_decision`; it is never PM write authorization;
- a **recipient** — an asset creator or human QA tester receives a packet;
- an **issue shape** — an asset request is an `output.draft_issue`.

Adding an actor requires a genuinely new execution surface, never a new role.
The operative rule lives in `kernel/actors.json` (`actor_model_note`); this ADR
is the durable record of why.

## Consequences

- Routing a review/QA/security/asset task chooses an existing surface and a
  workflow/output; it never invents an actor (`templates/prompts/review-pr.md`
  already forbids inventing `actor.reviewer_chat`).
- `boundary.security_privacy` always applies regardless of who reviews.
- A first-class QA/asset/security template or output contract is added only if a
  separately scoped issue records a real, observed failure it would prevent.
- Tooling that consumes Project OS must store the resolved actor as one of the
  four surfaces, not as a role.
