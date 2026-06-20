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

## What it is — and is not

It **is** a behavior kernel: small JSON files an agent *reads* to resolve how to
act, plus a portability protocol and copy-in adapter/templates. It is **not** a
runtime, service, database, agent framework, or prompt pack — there is nothing to
install or run. It does not act for you, store project state, grant permissions,
or automate merges, releases, or any PM decision. Capability comes from the
execution surface, never a role.

## Repository map

| Path | Purpose | Canonical? |
| --- | --- | --- |
| `kernel/*.json` | The operating kernel: actors, execution modes, boundaries, evidence, workflows, outputs, statuses | **Canonical** |
| `tools/` + `tests/` | The single kernel validator, read-only auditors, and tests | **Canonical** |
| `docs/TRACEABILITY_PROTOCOL.md` | The live-state / portability rules | **Canonical** |
| `AGENTS.md`, `CLAUDE.md` | This repo's own adapters (it runs on its own kernel) | Adapter (self) |
| `adapters/*.target.md` | Copy-me adapter templates to adopt the kernel in another repo or chat | Template |
| `templates/*.md` | Fill-in shapes: `artifacts.md` (issue, PR, closure, ADR, roadmap), `route-prompt.md`, `pm-command-bundle.md` | Template |
| `docs/DESIGN.md` | Background: why the kernel is shaped this way, the actor model, and its history | Background |

A cold reader needs only the **Canonical** rows to operate. Adapters and
templates are copied/filled per project; the background doc is optional.

**Self vs target adapters:** the root `AGENTS.md` / `CLAUDE.md` are *this* repo's
live adapters. The `adapters/*.target.md` files are blank templates you copy into
*another* repo or chat — the `.target.md` suffix marks "copy me, fill me in."

**Naming convention:** adapter templates are `<SURFACE>.target.md`; kernel files
are `<family>.json`; templates are lowercase-kebab `.md`; docs are
`UPPER_SNAKE.md`. Each top-level folder has one purpose: `kernel/` (the kernel),
`adapters/` (adapter templates), `templates/` (fill-in shapes), `docs/` (prose
docs), `tools/` + `tests/` (validator and tests).

## How an agent resolves the kernel

Read `kernel/manifest.json` and follow its `resolution_sequence` exactly: resolve
the current actor (surface), apply boundaries, resolve the execution mode and
workflow, gather the required live evidence, and select the output contract.
Return exactly one of four statuses — `status.resolved`,
`status.needs_context`, `status.needs_pm_decision`, `status.blocked`.
Resolution selects shape and gates; it never grants permission. Fail closed on
anything missing or ambiguous.

## Booting each surface

- **Terminal agent (a repo):** copy `KERNEL_REPOSITORY`'s
  `adapters/AGENTS.target.md` (and optionally `adapters/CLAUDE.target.md`) into
  the target repo, fill the placeholders, and point `KERNEL_LOCAL_PATH` at this
  repo's `kernel/`.
- **Browser chat:** paste `KERNEL_REPOSITORY`'s
  `adapters/BROWSER_CHAT.target.md` into the chat's project instructions; for a
  one-off session, paste its "First-message activation" block as the first
  message. Browser chat is draft-only (`actor.browser_chat`); it routes
  write-capable work to a terminal agent.
- **Routing & PM ops:** route work with `KERNEL_REPOSITORY`'s
  `templates/route-prompt.md` (one template, four variants: implement, review,
  correct, audit); copy-safe PM command bundles follow
  `templates/pm-command-bundle.md`.

Target product truth stays in the target repository; the kernel owns only
generic operating behavior.

## Validation

```sh
python3 -m tools.validate_kernel   # the only kernel integrity validator
python3 -m pytest tests/ -q        # validator, auditor, and repo-shape tests
```

`tools.validate_kernel` is the only kernel integrity validator. It only
validates `kernel/*.json`.

`tools.audit_target_adapters` is a manual, explicit-target, read-only diagnostic
for repositories that adopt this kernel. It audits filled target adapters for
metadata, roadmap anchors, likely durable live state, and protected overlay
removals without editing the target:

```sh
python3 -m tools.audit_target_adapters --target /path/to/target --repository org/repo
```

`tools.audit_traceability` is a separate read-only GitHub traceability
diagnostic for explicitly selected issues, PRs, or bounded ranges. It reports
missing closure packets, validation evidence gaps, duplicate comments, and
likely PR scope drift without editing GitHub state:

```sh
python3 -m tools.audit_traceability --repository org/repo --issue 123 --json
```

CI (`.github/workflows/validate.yml`) runs kernel validation and the test suite
only. It must not run live target scans or audit external target repositories
automatically. It is self-check only — it makes no writes and automates no PM
authority (no merge, closure, labels, releases, or target mutation). The
repo-shape guards in `tests/test_validate_kernel.py` keep the repo compact: they
fail if console planning docs return, the actor model gains a role-actor, or a
command bundle uses an unsupported `gh --json` field.

## Background

This repo previously held a contract-graph architecture (781 contracts, ~5,000
lines of validators), reduced to this minimal kernel after a 2026-06 audit of
real usage. Rationale, the actor model, and recovery of the old tree from git
history: `docs/DESIGN.md`.
