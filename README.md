# project-os-v2-min

A compact, portable operating kernel for working with AI agents. A small set of
agent-resolvable JSON files tells any agent (Claude, Codex, ChatGPT, or a future
tool) **how to behave** on a project — actors, modes, boundaries, workflows,
evidence, outputs, statuses — while all **live project state stays in GitHub**.
Any agent can take over a project cold by resolving the kernel and reading
GitHub; nothing depends on a prior chat's memory.

## Source of truth

- **Stable behavior** lives in `kernel/*.json` (versioned, validated).
- **Live project state** (issues, PRs, branches, commits, reviews) lives only in
  GitHub, read at task time per `docs/TRACEABILITY_PROTOCOL.md`.
- Everything else (adapters, templates) only **boots** an agent into those two
  and shapes its output. Shape never grants permission.

## Repository map

| Path | Role | Canonical? |
| --- | --- | --- |
| `kernel/*.json` | The operating kernel: actors, execution modes, boundaries, evidence, workflows, outputs, statuses | **Canonical** |
| `tools/`, `tests/` | The single integrity validator and its tests | **Canonical** |
| `docs/TRACEABILITY_PROTOCOL.md` | The live-state / portability rules | **Canonical** |
| `docs/decisions/` | ADRs — decisions that outlive issues | **Canonical** (when present) |
| `AGENTS.md`, `CLAUDE.md` | This repo's own adapters (it runs on its own kernel) | Adapter |
| `adapters/*.target.md` | Copy-me templates to adopt the kernel in another repo or chat | Template |
| `templates/` | Output and prompt shapes (issue, PR, ADR, closure, roadmap, command bundle, route prompts) | Template |
| `docs/DESIGN.md`, `docs/MIGRATION_FROM_V2.md` | Background: why the kernel is shaped this way, and its history | Background |

A cold reader needs only the **Canonical** rows to operate. Adapters and
templates are copied/filled per project; background docs are optional.

Each top-level folder has one purpose: `kernel/` (the validated kernel),
`adapters/` (bootloader templates), `templates/` (artifact shapes, with prompt
shapes under `templates/prompts/`), `docs/` (prose docs + ADRs under
`docs/decisions/`), `tools/` + `tests/` (the validator and its tests). Naming
convention: adapter templates are `<SURFACE>.target.md`; kernel files are
`<family>.json`; other templates and prompts are lowercase-kebab `.md`; reference
docs are `UPPER_SNAKE.md`; ADRs are `ADR-NNNN-<slug>.md`.

## How an agent resolves the kernel

Read `kernel/manifest.json` and follow its `resolution_sequence` exactly: resolve
the current actor (surface), apply boundaries, resolve the execution mode and
workflow, gather the required live evidence, and select the output contract.
Return exactly one of four statuses — `resolved`, `needs_context`,
`needs_pm_decision`, `blocked`. Resolution selects shape and gates; it never
grants permission. Fail closed on anything missing or ambiguous.

## Booting each surface

- **Terminal agent (a repo):** copy `adapters/AGENTS.target.md` (and optionally
  `adapters/CLAUDE.target.md`) into the target repo, fill the placeholders, and
  point `KERNEL_LOCAL_PATH` at this repo's `kernel/`.
- **Browser chat:** paste `adapters/BROWSER_CHAT.target.md` into the chat's
  project instructions, or `templates/prompts/browser-chat-activation.md` as the
  first message for a one-off session. Browser chat is draft-only
  (`actor.browser_chat`); it routes write-capable work to a terminal agent.
- **Routing & PM ops:** reusable route prompts live in `templates/prompts/`;
  copy-safe PM command bundles follow `templates/pm-command-bundle.md`.

Target product truth stays in the target repository; the kernel owns only
generic operating behavior.

## Validation

```sh
python3 -m tools.validate_kernel   # kernel integrity (refs, statuses, budget, safety)
python3 -m pytest tests/ -q        # validator + repo-shape guards
```

CI (`.github/workflows/validate.yml`) runs the same two checks on every push and
pull request. It is self-check only — it makes no writes and automates no PM
authority (no merge, closure, labels, releases, or target mutation). The
repo-shape guards (`tests/test_repo_shape.py`) keep the repo compact: they fail
if console planning docs return, the actor model gains a role-actor, or a command
bundle uses an unsupported `gh --json` field.

## Background

This repository previously held a contract-graph architecture (781 contracts,
570 relationship files, a ~5,000-line validator suite). It was reduced to this
minimal kernel after an audit of real usage across six target projects.
Rationale: `docs/DESIGN.md`. What moved where: `docs/MIGRATION_FROM_V2.md`. The
full pre-transformation tree remains in git history.
