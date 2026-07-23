# project-os-v2

**Project OS is a compact, portable operating kernel for directing software
projects with AI agents without losing control.** A small set of
agent-resolvable JSON files defines **how to behave** — actors, modes,
workflows, boundaries, evidence, outputs and statuses — while **all live
project state stays in GitHub** and is read at task time. Any agent can resume
a project cold by resolving the kernel and reading GitHub; nothing depends on
one chat's memory.

There are two active, semantically equivalent surfaces: **`project-os-es/`**
(Spanish, default) and **`project-os-en/`** (English, explicit selection).
Omitting the kernel path always keeps Spanish.

**Versión en español:** [README.md](README.md).

## What it is and what it is not

Project OS is a **human-directed operating system** for building real
products with AI agents, preserving context, quality, traceability and
control: a GitHub-native process operating layer, anchored in concrete
workflows — issues, PRs, evidence, proportional validation,
review-before-close and exact PM decisions.

What it is **not**:

- It is not an automatic coding agent and it never leaves agents working
  unsupervised: the human keeps scope, approvals, merge, close and release.
- It is not a runtime, a hosted runner or a workflow engine.
- It is not a write-capable API or an operations console.
- It does not replace OpenAI Agents SDK, LangGraph/Deep Agents,
  AutoGen/Microsoft Agent Framework, Claude Code, Codex or GitHub: it is the
  process layer those tools execute under.

## Who it is for

- **People learning or vibe coding.** Understand what changed and why; catch
  errors an implementation agent missed; review, adjust scope and draft
  corrections from browser chat; learn debugging and QA from concrete
  evidence; continue work without depending on a previous chat's memory.
  Project OS is a structured complement to how you already work.
- **Experienced developers and small teams.** Explicit scope and transitions;
  independent review between implementation and closeout; clear summaries of
  changes, risks and validation; GitHub-native traceability; proportional
  validation; explicit authorization; freedom to switch agents and providers
  without losing project context to a single tool or context window.

The verifiable detail — benefits with their source in the tree, the modular
architecture, and scenarios such as chat loss, handoff, agent switching,
missing approval, out-of-scope corrections and human QA — lives in
[`project-os-en/docs/benefits.md`](project-os-en/docs/benefits.md).

## Sources of truth

- **Stable behavior** lives in `project-os-es/kernel/*.json` (versioned and
  guarded by tests).
- **Live project state** (issues, PRs, branches, commits, reviews) lives only
  in GitHub and is reconstructed at task time, per
  `project-os-en/docs/rules.md`.
- Everything else (adapters, operations, templates, docs) only **boots** an
  agent toward those two sources and shapes its output. Shape never grants
  permission (`boundary.output_not_permission`).

## Repository map

| Path | Purpose | Active? |
| --- | --- | --- |
| `project-os-es/kernel/*.json` | Spanish operating kernel: actors, modes, workflows, boundaries, evidence, outputs, statuses, artifacts and skills | **Active (default)** |
| `project-os-en/kernel/*.json` | Parallel English operating kernel, with the same IDs, gates and relationships | **Active (explicit)** |
| `tools/project_os_resolve.py` | Single principal deterministic resolver: Spanish by default, English via explicit path, never granting permission | **Active** |
| `project-os-en/docs/` | PM-facing docs: `project-os-en/docs/getting-started.md`, `project-os-en/docs/rules.md`, `project-os-en/docs/rhythm.md`, `project-os-en/docs/benefits.md`, `project-os-en/docs/context-benchmark.md` | **Active (explicit)** |
| `project-os-en/operations/` | Compact English MOSDLC catalog, by phase | **Active (explicit)** |
| `project-os-en/adapters/` | Adapter templates `*.target.md` to adopt Project OS on a target | **Active (explicit)** |
| `project-os-en/templates/` + `project-os-en/skills/` | Artifact shapes and optional skills referenced by the kernel | **Active (explicit)** |
| `project-os-es/docs/`, `operaciones/`, `adapters/`, `templates/`, `habilidades/` | The default Spanish PM-facing layers | **Active (default)** |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | This repo's own adapters (it runs on its own kernel) | Adapter (self) |
| `docs/decisions/` | This repository's ADRs | Repo decisions |
| `tools/` + `tests/` | Resolver and validator of the active kernel, focused guards and secondary read-only diagnostics | Active infrastructure |

The previous surface is not part of the current tree. When a historical audit
needs it, it is recovered exclusively from git history; it is not an operating
path or an active source.

## How an agent resolves the kernel

Read `project-os-en/kernel/manifest.json` and follow its
`resolution_sequence` exactly. Resolution returns exactly one status —
`status.resolved`, `status.needs_context`, `status.needs_pm_decision` or
`status.blocked` — selects shape and gates, and **grants no permission**. On
any missing or ambiguous input, it fails closed.

On a terminal surface with a local checkout and Python, the fast path is the
principal resolver (adoption details live in
`project-os-en/docs/getting-started.md`):

```sh
python tools/project_os_resolve.py --actor <actor> --workflow <workflow> \
  --mode <mode> --kernel-dir project-os-en/kernel [--skill skill.<id>]
```

The Spanish surface is the default: omit `--kernel-dir` or pass
`--kernel-dir project-os-es/kernel`. No persisted preference or global
language selector exists.

The resolver accepts `--hydration-level minimal|compact|full/debug`; `compact`
is the practical default. The level only projects how much already-resolved
contract is returned; it never changes authority or reads live state.
`full/debug` is for review, debugging or audit. The pre-existing `--compact`
flag remains JSON formatting only. Measured sizes per level, with declared
method, tokenizer and date, live in
[`project-os-en/docs/context-benchmark.md`](project-os-en/docs/context-benchmark.md).

Manual resolution from `project-os-en/kernel/manifest.json` remains the
canonical fallback. Browser/non-terminal surfaces never run repo-local
Python: they always resolve manually from the manifest. In both cases the
resolved output only shapes behavior and grants no permission.

## Quick start

Project OS delegates safe work to AI through compact operations, PM variables
and live GitHub traceability.

1. **Start with** `project-os-en/docs/getting-started.md`: surfaces, external
   prerequisites and the first session.
2. **Adopt the kernel on a target**: copy
   `project-os-en/adapters/AGENTS.target.md` to the target repo root
   (terminal) or use `project-os-en/adapters/BROWSER_CHAT.target.md` as the
   browser chat bootloader. Adoption is copy-based by design: no installer,
   package or CLI is required.
3. **Operate by phase**: the complete operations catalog is in
   `project-os-en/operations/README.md`; the day-to-day cycle in
   `project-os-en/docs/rhythm.md`; the non-negotiable rules in
   `project-os-en/docs/rules.md`.
4. **Optionally generate a local prompt**: run
   `python tools/operation_prompt_wizard.py --language en` (or answer its
   one-time `es/en` question; Spanish stays the default). The wizard loads
   the coherent bundle of that surface — operations, skills and orienting
   kernel — lists the active operations recursively, supports filtering and
   selection by index, MOS code (`MOS-3.5`), filename, stem or relative path,
   and only writes the local artifact you confirm. The selection lives only
   in the wizard session and never adopts, installs or configures a target.

## Validation

```sh
python3 -m tools.validate_kernel --kernel-dir project-os-es/kernel
python3 -m tools.validate_kernel --kernel-dir project-os-en/kernel
python3 -m pytest tests/ -q
python3 -m pytest dogfooding/tests/ -q
```

The tree physically separates three layers:

- **Portable core** (`project-os-es/`, `project-os-en/`, `tools/`, `tests/`):
  kernel, operations, templates, skills, resolver, wizard, validator and their
  behavioral tests. This is what a target adopts; it never depends on
  `dogfooding/`.
- **Adapters** (`project-os-*/adapters/` and `tools/audit_traceability.py`):
  GitHub/git/filesystem surfaces a target may use or omit.
- **`project-os-v2` dogfooding** (`dogfooding/`): tooling, tests and
  documentation exclusive to maintaining this repository — ES/EN parity
  (`dogfooding/tools/project_os_parity.py`), target adapter audits
  (`dogfooding/tools/audit_target_adapters.py`), the resolution-size
  diagnostic, repository-shape guards, and the internal-handoff and
  publication-readiness docs. A target inherits nothing from this layer.

`tests/test_active_project_os_resolver.py` guards the active Spanish kernel
resolution and prevents active references to the removed resolver.
`dogfooding/tests/test_project_os_bilingual_parity.py` guards ES/EN structural
parity, MOS contracts, adapters, paths and fail-closed selection.
`tools.validate_kernel` validates the selected allowed surface; Spanish stays
its default when `--kernel-dir` is omitted.

`dogfooding.tools.audit_target_adapters` and `tools.audit_traceability` remain
manual read-only diagnostics. CI (`.github/workflows/validate.yml`) runs only
the validation and the two test suites: it performs no writes and automates no
PM authority.

## Background

This repo previously held a contract-graph architecture (781 contracts),
reduced to the minimal English kernel after a real-usage audit in 2026-06 and
then consolidated on the Spanish surface `project-os-es` as the primary base
(ADR 0003, `docs/decisions/0003-project-os-cli-adoption-model.md`). The
history and rationale of retired surfaces are recoverable from git; the
current tree keeps Spanish as the default with its parallel English
translation.

By durable decision (ADR 0005,
`docs/decisions/0005-public-repository-strategy.md`), this repository stays
private as CodeFusion's internal baseline; the future public surface of
Project OS is a separate repository with its own public-readiness gate. The
documentation and onboarding in this tree stay reusable by that surface.

## Security, contributions, support and conduct

- [SECURITY.md](SECURITY.md) — responsible vulnerability reporting, always
  through a private channel.
- [CONTRIBUTING.md](CONTRIBUTING.md) — issue-first contribution process, in
  Spanish or English, inbound=outbound under Apache-2.0.
- [SUPPORT.md](SUPPORT.md) — best-effort support, no SLA.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — Contributor Covenant 3.0.

## License

Copyright 2026 CodeFusion SpA.

This repository is distributed under the [Apache License 2.0](LICENSE)
(SPDX: `Apache-2.0`). The license covers the code, the kernel JSON, the
templates, the operations and the documentation in the tree.

The license authorizes nothing else by itself: publication, visibility,
support, contributions and releases stay subject to their own gates and PM
decisions (see `dogfooding/docs/security/PUBLIC_READINESS_REVIEW.md`).
