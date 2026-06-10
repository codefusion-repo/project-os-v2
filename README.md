# project-os-v2-min

The minimal operating kernel for Project OS: a small set of agent-resolvable
JSON files that tell any AI agent (Claude, Codex, ChatGPT, or future tools)
**how to behave** on a project, while all live project state stays in GitHub.

## The three layers

| Layer | Where | Role |
| --- | --- | --- |
| Kernel | `kernel/*.json` (~25KB, hard 100KB budget) | Stable behavior: actors, execution modes, boundaries, workflows, evidence, outputs, statuses |
| Live traceability | GitHub issues/PRs/commits/comments | The only live state; lets any agent take over a project cold (`docs/TRACEABILITY_PROTOCOL.md`) |
| Adapters & templates | `AGENTS.md`, `CLAUDE.md`, `adapters/`, `templates/` | Thin bootloaders and output shapes |

## How an agent uses it

Read `kernel/manifest.json` and follow its `resolution_sequence`:
surface → actor → execution mode → boundaries → workflow → evidence → output
contract → status. Exactly one of four statuses is returned: `resolved`,
`needs_context`, `needs_pm_decision`, `blocked`. Resolution selects shape and
gates; it never grants permission.

## Validation

```sh
python3 -m tools.validate_kernel   # kernel integrity (refs, statuses, budget, safety)
python3 -m pytest tests/ -q        # validator test suite
```

## Adopting in a target project

Copy `adapters/AGENTS.target.md` (and optionally `adapters/CLAUDE.target.md`)
into the target repository, fill the placeholders, and point
`KERNEL_LOCAL_PATH` at this repository's `kernel/`. Target product truth stays
in the target; the kernel owns only generic operating behavior.

## Background

This repository previously held a contract-graph architecture (781 contracts,
570 relationship files, a 5,000-line validator suite). It was transformed into
v2-min after an audit of real usage across six target projects. Rationale:
`docs/DESIGN.md`. What moved where: `docs/MIGRATION_FROM_V2.md`. Roadmap and
dogfood plan: the open `[ROADMAP][FIXED] project-os-v2-min` issue.
