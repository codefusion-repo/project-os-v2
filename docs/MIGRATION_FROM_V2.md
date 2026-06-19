# Migration: project-os-v2 → project-os-v2-min

## What happened

In June 2026, after a full audit of project-os, project-os-v2, and the real
target projects, project-os-v2 was transformed from a contract-graph
architecture into the minimal kernel described in `docs/DESIGN.md`. The fixed
roadmap for the transformation and what follows is the roadmap issue created
for v2-min (supersedes the previous 17-cycle roadmap issue).

## Where the old tree lives

Nothing was lost. The complete pre-transformation tree (781 contracts, 28
schema files, the 5,000-line validator suite, 122 test fixtures, and the
original design docs) is preserved in git history.

- Baseline: the last commit before the transformation branch
  (`MIN.0 Remove superseded v2 contract graph...` lists it in its message).
- Recover any path with: `git log --oneline -- <path>` and
  `git checkout <baseline-sha> -- <path>`.
- GitHub issues #1–#244 and the merged PRs remain the full historical record
  of how and why the old architecture was built.

## What was kept (normalized into the kernel)

| Old concept | Where it lives now |
| --- | --- |
| Actor types and surface boundaries | `kernel/actors.json` |
| Execution modes | `kernel/execution_modes.json` |
| Hard limits / boundary sets (límite) | `kernel/boundaries.json` |
| Evidence profiles (evidencia/fuente) | `kernel/evidence.json` |
| Workflow profiles and step ordering | `kernel/workflows.json` (steps inline) |
| Output contracts / plantillas | `kernel/outputs.json` + `templates/` |
| Resolver statuses and fail-closed model | `kernel/statuses.json` |
| Manifest / policy / selector bundles | `kernel/manifest.json` |
| No-live-state philosophy | `boundary.no_live_state_durable` + `docs/TRACEABILITY_PROTOCOL.md` |
| Validator suite intent | `tools/validate_kernel.py` (integrity only) |

## What was removed and why

| Removed | Why |
| --- | --- |
| `contracts/relacion/` (570 files, one per graph edge) | Nothing consumed the graph; relationships agents need are inline refs in kernel entries |
| `contracts/contrato/` (19 meta-contracts) | Contracts about contracts; no consumer |
| Remaining entity-family contracts (rol, regla, accion, recurso, scope, variable, estado, artefacto, resolver_output, …) | Mostly draft placeholders (585/781 draft, 740/781 without description); the operative content was distilled into the kernel |
| `schemas/` (28 files) and the in-house JSON Schema subset implementation | The single validator checks structure directly; a schema system for 8 files is overhead |
| `project_os_v2/validators/` (5,000 lines) and its 2,243-line test suite | Validated meta-process consistency of a graph no runtime read; replaced by `tools/validate_kernel.py` |
| The 17-cycle roadmap (#92) | Put first real use ~14 cycles away; replaced by the 4-phase v2-min roadmap with kill criteria |

## What stayed untouched

- All git history, issues, PRs, and review evidence. The complete
  pre-transformation tree — including `fuentes/`, the PM-provided source
  documents for the original entity model — is recoverable from git history.
