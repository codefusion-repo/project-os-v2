# Live Traceability Protocol

This protocol is what makes a project portable between AI agents. Any agent
(Claude, Codex, Gemini, ChatGPT, or a future tool) must be able to take over a
project cold and reconstruct what happened, what is missing, why, with what
evidence, and under what limits — from GitHub alone, never from another model's
internal memory.

State is **reconstructed from evidence, not recalled**. Recall can hallucinate;
evidence can be re-read.

## The seven rules

1. **Reconstruct before acting.** Before non-trivial work, read the live state
   from GitHub and git: the current issue, linked PRs, recent commits, the
   project's canonical roadmap issue, and relevant ADRs. Do not trust internal
   memory, prior-session context, or durable files for live state.

2. **Every issue carries its own context.** Issues follow
   `templates/artifacts.md` (Issue): why it exists, objective, source basis (links to the
   decisions and work it builds on), scope, out of scope, acceptance criteria,
   validation expectations.

3. **Every closure leaves a reconstruction packet.** No issue closes without a
   closure comment per `templates/artifacts.md` (Closure comment): completion evidence,
   validation evidence with real output, boundaries preserved (what was
   deliberately not done), accepted scoped validation/CI exceptions when
   present, a concise friction note, and commit/PR references.

4. **Every PR documents its own verification.** PR bodies follow
   `templates/artifacts.md` (Pull request): summary, scope and boundaries,
   validation commands with results or scoped PM/manual validation evidence,
   security/privacy notes, linked issue. Validation is proportional per
   `docs/VALIDATION_POLICY.md`; broad suites are not required when the issue
   risk does not justify them.

5. **One canonical roadmap issue per project.** It answers "what comes next
   and why" and is updated by superseding, not by storing mutable status.
   Decisions that outlive issues become ADRs (`templates/artifacts.md`, ADR).

6. **No live state in durable files.** Repository docs, kernels, and adapters
   never store issue/PR/branch/validation state, SHAs, or release readiness
   (kernel boundary `boundary.no_live_state_durable`). GitHub is the only live
   state store.

7. **Branches tie code to issues.** Work happens on `work/<issue>-<slug>`
   branches, so any agent can map code to its issue and back.

## Why this works

- GitHub is tool-neutral: any agent with `gh` reads the same state the PM reads.
- Evidence is versioned, timestamped, and auditable; memory is not.
- A new agent inherits documented facts, not the previous agent's mistakes.

## What this protocol is not

It is not a writing ritual. Each artifact exists for the next cold reader. If a
section does not help a cold agent reconstruct state or verify a claim, leave
it out.
