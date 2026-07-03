# Context economy and subagent discipline

Canonical home for `boundary.context_economy`: how Project OS agents keep
token/context/subagent overhead proportional to the scoped task, on every
surface and in every target repository. The kernel keeps only the hard floor;
adapters, route prompts, operation templates, and reports point here and never
restate these rules. This file stores no live state.

Economy is subordinate to safety. Nothing here drops required evidence, live
traceability reads (docs/TRACEABILITY_PROTOCOL.md), branch preflight,
validation, secret safety, or exact PM approval gates. When economy and a
required gate conflict, the gate wins.

## Context classes

Classify context before reading, passing, or restating it:

1. **Read live; never from memory or paste.** Issue/PR objective, scope,
   comments, reviews, diffs, branch and worktree state, checks, the roadmap
   issue, ADRs, and validation output. Live state is reconstructed from GitHub
   and git at task time; a pasted copy is a stale claim, not evidence.
2. **Cite or summarize.** Prior reports, closed discussions, long documents,
   and any source the reader can re-open: reference the location (issue/PR
   number, path, `file:line`) plus the minimal excerpt the task needs.
3. **Do not paste repeatedly.** Full issue bodies, full diffs, full logs,
   full prior reports, resolver output already available to the reader, and
   rules the kernel or a canonical doc already owns. Restating them costs
   tokens, drifts from the source, and creates competing sources of truth.
4. **Justified larger context.** Security review, authorization or
   secret-adjacent changes, deployment, data migration, billing/storage,
   complex architecture, and multi-file protocol changes justify reading and
   quoting more evidence. Scope the extra context to the risk under review;
   never suppress context that high-risk work needs.

## Subagent discipline

- Subagents are not the default. Do simple, local, or single-surface work
  directly.
- Use a subagent only with a scoped reason: it materially reduces risk,
  complexity, or expert review burden — for example a broad multi-location
  search, an independent security or review pass, or an isolated long-running
  task whose intermediate output the main task does not need.
- Hand a subagent a compact evidence packet: the task, exact scope and
  out-of-scope, the specific paths/ids/refs it needs, and where to read live
  state — not the full conversation, issue body, diff, or prior reports.
- Summarize subagent output compactly, and treat it as claims or evidence
  leads, not proof: verify it against live issue/PR/code/diff/validation
  evidence before acting on it or reporting it, exactly as
  `boundary.review_before_close` treats PR bodies and comments.
- Do not chain subagents into a hidden workflow engine; kernel workflows
  remain the flow, and every boundary and approval gate applies inside a
  subagent exactly as it does outside.

## Handoffs and reports

- Route prompts stay compact and issue-referential (templates/route-prompt.md):
  the executing agent reads the issue live; SCOPE and OUT_OF_SCOPE are 1-3
  lines, never the body.
- Reports follow their output contract and stay complete enough for review,
  citing live evidence (issue/PR, `file:line`, commands with results) instead
  of restating full source bodies or prior reports.
- Validation evidence is the commands run and their real results; quote the
  result line and any failure detail, not full unabridged logs, unless the
  failure itself needs them.
- Repeated resolver or kernel guidance is never pasted between agents: the
  receiving agent resolves the kernel itself.

## Boundaries with adjacent policies

- What validation to run, and when, is owned by
  `boundary.validation_discipline` (proportional validation); this file adds
  nothing to it.
- Compacting MOSDLC operation templates and moving repeated template guidance
  into resolver ownership is separate post-MOSDLC work; this file governs
  agent behavior at task time and rewrites no operation templates.
