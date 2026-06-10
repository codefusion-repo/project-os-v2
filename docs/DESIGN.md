# project-os-v2-min — Design

## What this is

project-os-v2-min is the minimal operating kernel for Project OS: the smallest
set of files that lets any AI agent resolve **how to behave** before acting on
a project, while all live project state stays in GitHub.

It replaces the previous project-os-v2 contract-graph architecture (781
contracts across 18 entity families, 570 relationship files, ~5,000 lines of
meta-process validators). See `docs/MIGRATION_FROM_V2.md`.

## Evidence basis

A full audit (2026-06) of project-os, project-os-v2, and six real target
projects established what actually delivers value in practice:

1. **The resolvable kernel.** Real agent sessions (Codex on salvation) resolve
   the v1 JSON kernel before editing: actor, workflow, execution mode,
   boundaries, evidence, outputs. The kernel is operationally consumed. But the
   v1 hot path costs ~472KB per resolution across 8 registries, and another
   ~597KB of registries shows no evidence of being read at all.
2. **Live GitHub traceability.** Issue source-basis chains, closure-evidence
   comments, and PR validation bodies let any agent reconstruct project state
   cold. This is the portability layer between AI tools.
3. **Thin prose adapters.** AGENTS.md/CLAUDE.md bootstrap any agent into 1 and 2.

What did **not** deliver value: the v2 normalized relationship graph (nothing
consumed it), meta-contracts, validator hardening against risks that cannot
materialize without a runtime, and micro-granular process issues.

## Design rules

- **The consumer is an LLM.** Kernel files are optimized for cheap, unambiguous
  reading by agents, not for relational normalization. Prose-bearing JSON with
  stable ids beats a normalized graph.
- **Hard size budget.** The kernel must stay under 100KB total (target 60KB);
  the validator fails it otherwise. Current size: ~25KB — a ~95% reduction
  against the v1 hot path. Growth requires shrinking something else.
- **One validator.** `tools/validate_kernel.py` checks integrity (references,
  canonical statuses, no permission grants, no live state, actor safety, size
  budget). There is no other validation layer. Validators guard the kernel;
  they do not model the process.
- **Three layers, strictly separated.**
  - `kernel/` — stable behavior (versioned, validated).
  - GitHub — live state (`docs/TRACEABILITY_PROTOCOL.md`).
  - `AGENTS.md` / `CLAUDE.md` / `adapters/` / `templates/` — boot and shape.
- **Fail closed.** Exactly four resolution statuses; ambiguity never proceeds.
- **No runtime until dogfood demands it.** No loader, resolver runtime,
  automation, or panel work unless real-target evidence (roadmap phases MIN.1–
  MIN.3) names a gap that prose plus kernel resolution cannot close.

## Kernel resolution model

An agent resolves, in order: surface → actor → execution mode → boundaries →
workflow → evidence → output contract → status. The sequence is data in
`kernel/manifest.json`; the agent executes it by reading, not by running code.
Resolution selects shape and gates; it never grants permission.

## Anti-bureaucracy guardrails

Lessons from the audit, encoded as rules:

- One issue per outcome; no `[Review]` issue before every implementation issue.
- Issue bodies under ~5KB; out-of-scope lists name only plausible mistakes.
- Boundaries live in the kernel (read once per session), not restated in every
  issue.
- New kernel entries, validators, or process artifacts require a named,
  observed failure they would have prevented.
