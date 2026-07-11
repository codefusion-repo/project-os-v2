# Project OS — English surface

`project-os-en/` is the explicitly selected English surface parallel to `project-os-es/`. It has the same stable kernel IDs, gates, MOS codes, variables, references, and responsibilities. Human-facing prose and paths are English. Spanish remains the repository default.

## Topology and ownership

- `kernel/`: English kernel JSON, selected explicitly with `--kernel-dir project-os-en/kernel`.
- `docs/`: compact PM-facing orientation, rules, and lifecycle rhythm.
- `operations/`: the complete English MOSDLC catalog under `cross-phase/` and `phase-*`.
- `adapters/`: one complete `AGENTS` bootloader, Claude/Gemini shims, and a read-only browser adapter.
- `templates/`: artifact forms referenced by `kernel/artifacts.json`.
- `skills/`: optional capabilities referenced by `kernel/skills.json`; never workflow logic or authorization.

The single principal resolver is `tools/project_os_resolve.py`. Omitting `--kernel-dir` selects Spanish; English must be explicit. No language preference or global selector is stored.
