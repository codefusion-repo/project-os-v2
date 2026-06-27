# project-os-v2-min — Design

## What this is

project-os-v2-min is the minimal operating kernel for Project OS: the smallest
set of files that lets any AI agent resolve **how to behave** before acting on
a project, while all live project state stays in GitHub.

It replaces the previous project-os-v2 contract-graph architecture (781
contracts across 18 entity families, 570 relationship files, ~5,000 lines of
meta-process validators). See the History section below.

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
3. **Thin prose adapters.** AGENTS.md/CLAUDE.md/GEMINI.md bootstrap any agent into 1 and 2.

What did **not** deliver value: the v2 normalized relationship graph (nothing
consumed it), meta-contracts, validator hardening against risks that cannot
materialize without a runtime, and micro-granular process issues.

## Design rules

- **The consumer is an LLM.** Kernel files are optimized for cheap, unambiguous
  reading by agents, not for relational normalization. Prose-bearing JSON with
  stable ids beats a normalized graph.
- **Hard size budget.** The kernel must stay under 100KB total (target 60KB);
  the validator fails it otherwise. It currently sits at a small fraction of the
  budget — roughly a 95% reduction against the v1 hot path. Growth requires
  shrinking something else.
- **One validator.** `tools/validate_kernel.py` checks integrity (references,
  canonical statuses, no permission grants, no live state, actor safety, size
  budget). There is no other validation layer. Validators guard the kernel;
  they do not model the process.
- **Three layers, strictly separated.**
  - `kernel/` — stable behavior (versioned, validated).
  - GitHub — live state (`docs/TRACEABILITY_PROTOCOL.md`).
  - `AGENTS.md` / `CLAUDE.md` / `GEMINI.md` / `adapters/` / `templates/` — boot and shape.
- **Fail closed.** Exactly four resolution statuses; ambiguity never proceeds.
- **No kernel runtime.** No loader, resolver runtime, or automation belongs in
  this kernel unless real-target evidence and a scoped issue name a gap that
  prose plus kernel resolution cannot close. Any future tooling built over
  Project OS must consume these semantics; it must not replace them or become a
  second source of truth.

## Kernel resolution model

An agent follows the `resolution_sequence` in `kernel/manifest.json`. The
sequence is data in the manifest; adapters and docs point to it instead of
owning a parallel copy. The agent executes it by reading, not by running code.
Resolution selects shape and gates; it never grants permission.

## Actor model

Capability comes from the **execution surface**, never from a role. The four
actors in `kernel/actors.json` (`human_pm`, `terminal_agent`, `browser_chat`,
`unknown`) are the only actors. Reviewer, QA, asset creator, and security
reviewer were once floated as candidate actors; they are deliberately **not**
actors. Each is a review focus (a security/QA review is
`workflow.review_before_close` or `workflow.review_only` on an existing
surface), a gate (a QA/security verdict is evidence that can return
`status.needs_pm_decision`, never write authorization), a recipient (a human QA
tester or asset creator receives a packet), or an issue shape (an asset request
is an `output.draft_issue`). Adding an actor requires a genuinely new execution
surface, not a new role — and, per the guardrail below, a named observed failure.
The operative rule is the `actor_model_note` in `kernel/actors.json`.

## Anti-bureaucracy guardrails

Lessons from the audit, encoded as rules:

- One issue per outcome; no `[Review]` issue before every implementation issue.
- Issue bodies under ~5KB; out-of-scope lists name only plausible mistakes.
- Boundaries live in the kernel (read once per session), not restated in every
  issue.
- New kernel entries, validators, or process artifacts require a named,
  observed failure they would have prevented.

## Where each kind of thing belongs

When unsure where something goes, this is the order of precedence:

- **Kernel (`kernel/*.json`)** — stable, generic operating behavior only:
  actors, modes, boundaries, workflows, evidence, output shapes, statuses.
  Versioned and validated. No live state, no permission grants.
- **Adapters (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `adapters/`)** — compact per-repo/chat
  bootloaders: identity, kernel path, a pointer to the canonical roadmap, a
  short notes block. No kernel-rule duplication, no live state.
- **Templates (`templates/`)** — reusable output and prompt shapes. Shape only.
  PM command-bundle style lives in exactly one source,
  `templates/pm-command-bundle.md`.
- **Roadmap issue** — one canonical roadmap per project: what comes next and
  why. Superseded, not mutated into a status store.
- **ADR** — decisions that outlive issues, in the repo that owns the decision,
  using the ADR shape in `templates/artifacts.md`.
- **Target repo** — all product, domain, runtime, build, and validation truth
  for a target. The kernel never stores target product facts.

## History

project-os-v2 previously held a contract-graph architecture: 781 contracts
across 18 entity families, 570 one-per-edge relationship files, 28 schema files,
and a ~5,000-line meta-process validator suite with a 2,243-line test suite. A
2026-06 audit found nothing consumed the relationship graph or the
meta-contracts, and the validators guarded a process no runtime executed. It was
reduced to this kernel: actor/mode/boundary/evidence/workflow/output/status
behavior distilled into `kernel/*.json`, the no-live-state philosophy into
`boundary.no_live_state_durable` plus `docs/TRACEABILITY_PROTOCOL.md`, and the
validator intent into `tools/validate_kernel.py` (integrity only).

Nothing was lost: the complete pre-transformation tree — contracts, schemas,
validators, fixtures, the original `fuentes/` source documents, and all issues
and PRs — remains in git history. Recover any path with
`git log --oneline -- <path>` then `git checkout <baseline-sha> -- <path>`.
