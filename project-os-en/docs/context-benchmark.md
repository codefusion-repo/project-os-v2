# Reproducible context benchmark

**How much instruction context an agent session loads at start, measured over
real, publicly verifiable conventional stacks and over the Project OS stack,
against one declared task.** This benchmark reports sizes and, in its
coverage matrix, observed presence of instructions: it does not measure
quality, it ranks no stack, it does not demonstrate savings against any
stack, it promises no universal savings, and it grants no permission
(`boundary.output_not_permission`).

Spanish version: [benchmark-contexto.md](../../project-os-es/docs/benchmark-contexto.md).

## Declared task and unit of measurement

- **Declared task:** govern a terminal coding agent implementing a scoped
  work unit inside a repository.
- **Unit of measurement (functional equivalence):** the repo-wide instruction
  files each tool loads by convention at the start of every session, before
  any live task data. On-demand context in each stack (subdirectory
  `CLAUDE.md` files, `applyTo`-scoped instructions, skills, MOS operations)
  stays out: it loads only when used.
- **Project OS session stack:** the `CLAUDE.md` shim + the `AGENTS.md`
  bootloader + resolver stdout with `--hydration-level compact --compact` at
  the tuple `actor.terminal_agent` / `workflow.issue_implementation` /
  `mode.delegated_commit_pr`.

## Declared method

- **Measurement date:** 2026-07-14.
- **Local inputs:** commit `84a615d2b838` of `codefusion-repo/project-os-v2`;
  the measured inputs (`CLAUDE.md`, `AGENTS.md`, and both kernel directories)
  do not change after that commit on the branch correcting this document.
- **Public corpus:** every corpus item is measured exactly as it exists in its
  source repository at the commit pinned in the provenance table; nothing is
  copied into this repository and reproduction downloads each item from that
  commit.
- **Metrics:** UTF-8 bytes, characters, and tokens.
- **Declared tokenizer:** `tiktoken` 0.13.0 (Python 3.12.13), with two public
  encodings to show cross-tokenizer variation: `o200k_base` and `cl100k_base`.
  Token counts depend on the tokenizer and the model: no number in these
  tables is a universal saving.
- **Selected kernel vs live project data:** resolver output contains only
  already-resolved kernel contract. It includes no issues, PRs, branches,
  diffs, or any other live project data — that is read from GitHub at task
  time and stays outside this measurement by design.

## Main benchmark — public conventional stacks

### Selection criteria, declared before measuring

1. **Mechanisms:** the repo-wide instruction files with a vendor-documented
   convention in the first-party terminal coding agents from Anthropic,
   OpenAI, Google, and GitHub: Claude Code (`CLAUDE.md`), Codex CLI
   (`AGENTS.md`), Gemini CLI (`GEMINI.md`), and GitHub Copilot
   (`.github/copilot-instructions.md`).
2. **File per mechanism:** the one in the tool's own public repository when
   published at its canonical location; otherwise, the one in the
   highest-starred public repository of the vendor's GitHub organization that
   does publish it. Selected at the default branch HEAD on the measurement
   date and pinned by commit.
3. **Outcomes of applying that rule:** `openai/codex`,
   `google-gemini/gemini-cli`, and `microsoft/vscode-copilot-chat` publish
   their own file. `anthropics/claude-code` publishes no root `CLAUDE.md`, so
   the fallback selected `anthropics/claude-cookbooks`, that organization's
   highest-starred repository publishing one on the measurement date. Cursor
   rules dropped out through the rule itself: its vendor publishes no
   repository with verifiable `.cursor/rules` content.

### Corpus: provenance and licenses

| Stack | Measured file | Repository | Commit | License |
| --- | --- | --- | --- | --- |
| Claude Code | `CLAUDE.md` | `anthropics/claude-cookbooks` | `67ce644d33e5` | MIT |
| Gemini CLI | `GEMINI.md` | `google-gemini/gemini-cli` | `fa975395bcc6` | Apache-2.0 |
| GitHub Copilot | `.github/copilot-instructions.md` | `microsoft/vscode-copilot-chat` | `5863f5a70889` | MIT |
| Codex CLI | `AGENTS.md` | `openai/codex` | `393f64565ab4` | Apache-2.0 |

### Results

| Session stack | Bytes | Characters | Tokens `o200k_base` | Tokens `cl100k_base` |
| --- | ---: | ---: | ---: | ---: |
| Claude Code — `claude-cookbooks` | 3520 | 3520 | 914 | 914 |
| Gemini CLI — `gemini-cli` | 4610 | 4610 | 1140 | 1140 |
| GitHub Copilot — `vscode-copilot-chat` | 17401 | 17393 | 3970 | 3832 |
| Codex CLI — `codex` | 22519 | 22485 | 5182 | 5160 |
| Project OS — Spanish kernel (default) | 17815 | 17789 | 4195 | 4563 |
| Project OS — English kernel (explicit selection) | 16981 | 16960 | 3831 | 3899 |

Project OS stack breakdown in bytes: `CLAUDE.md` 296 + `AGENTS.md` 2301 +
resolver `compact` 15218 (Spanish kernel) or 14384 (English kernel).

### Reading these results

- The Project OS session stack falls **inside the observed range** of the
  real conventional stacks (3520–22519 bytes; 914–5182 `o200k_base` tokens):
  bigger than two of the four and smaller than the other two. This benchmark
  **demonstrates no saving** over conventional stacks and must not be cited
  as if it did.
- What differs is the kind of content, not primarily the size: the measured
  conventional files carry project engineering knowledge as prose (build,
  tests, style, architecture); the Project OS stack carries an
  already-resolved per-tuple contract (rules, boundaries, required inputs,
  outputs, and statuses, with explicit non-authorization). Which one fits
  depends on the project: this benchmark does not decide that and does not
  claim Project OS replaces any of these tools.

## Governance coverage matrix — same pinned corpus

This matrix records **observed presence of instructions** per criterion in
the same five stacks of the main benchmark: each conventional file exactly as
it exists at the pinned commit of the provenance table, and the Project OS
session stack (shim + bootloader + resolved `compact` kernel). Recording
presence measures no quality and weighs no criterion: the matrix is not a
ranking, and more Yes cells make no stack better.

### Legend

- **Yes:** the measured file contains explicit instructions on the criterion.
- **Partial:** the measured file covers the criterion only in a narrow or
  single-case way; the per-criterion evidence names which one.
- **Not observed:** the criterion does not appear in the measured file at its
  pinned commit. It means absence in that file, **not** tool incapacity:
  every one of these tools can cover the criterion with more files,
  configuration, or product, and that stays outside this measurement.
- **Not applicable:** the criterion is a property the measured file does not
  aim to have by design.

### Matrix

| Criterion | Claude Code — `claude-cookbooks` | Gemini CLI — `gemini-cli` | GitHub Copilot — `vscode-copilot-chat` | Codex CLI — `codex` | Project OS — session stack |
| --- | --- | --- | --- | --- | --- |
| Technical knowledge of the target | Yes | Yes | Yes | Yes | Partial |
| Security | Partial | Not observed | Not observed | Partial | Yes |
| Work-unit scope | Not observed | Partial | Not observed | Partial | Yes |
| Human authority per action | Not observed | Not observed | Not observed | Partial | Yes |
| Working-tree preflight | Not observed | Not observed | Not observed | Not observed | Yes |
| Required inputs before acting | Not observed | Not observed | Not observed | Not observed | Yes |
| Validation before delivering | Yes | Yes | Yes | Yes | Yes |
| Fail-closed | Not observed | Not observed | Partial | Not observed | Yes |
| Review-before-close | Not observed | Not observed | Partial | Partial | Yes |
| Work traceability | Partial | Yes | Not observed | Not observed | Yes |
| Governance portability | Not applicable | Not applicable | Not applicable | Not applicable | Yes |
| On-demand loading | Yes | Yes | Yes | Yes | Yes |
| Contract / live-state separation | Not observed | Not observed | Not observed | Not observed | Yes |

### Evidence per criterion

Each entry defines the criterion and cites the evidence behind every Yes,
Partial, or Not applicable cell; a Not observed cell is verified by reading
the whole file at the pinned commit, because it asserts an absence in that
file.

1. **Technical knowledge of the target** — build, tests, style, and
   architecture of the governed project. `claude-cookbooks`: the "Quick
   Start", "Development Commands", "Code Style", and "Project Structure"
   sections. `gemini-cli`: "Project Overview", "Building and Running", and
   "Testing and Quality". `vscode-copilot-chat`: "Project Overview", "Project
   Architecture", and "Coding Standards". `codex`: crate conventions and
   `just` commands in the root section, plus "TUI style conventions".
   Project OS (Partial): the `AGENTS.md` bootloader carries repository
   identity and stable repository notes; target engineering knowledge is
   reconstructed from live sources and stays outside the measured stack by
   design.
2. **Security** — handling of secrets, sensitive data, or a restricted
   environment. `claude-cookbooks` (Partial): "Key Rules" forbids committing
   `.env` and requires keys via the environment, with no general secrets
   policy. `codex` (Partial): rules about its sandbox (`CODEX_SANDBOX*`),
   with no secrets policy. Project OS: `rule.secret_safety` and
   `boundary.security_privacy`, including `[REDACTED]` redaction.
3. **Work-unit scope** — keeping the change inside one bounded work unit.
   `gemini-cli` (Partial): "Development Conventions" asks small, focused PRs.
   `codex` (Partial): "Change size guidance" caps change size and asks
   staged splits. Project OS: `evidence.issue_scope` (live objective, scope,
   out of scope, and acceptance criteria) and
   `boundary.implementation_discipline`.
4. **Human authority per action** — actions requiring explicit human
   approval. `codex` (Partial): asks the user before the full test suite and
   exempts `just fmt` from approval. Project OS: `rule.no_autorizacion`,
   `boundary.separate_pm_approval`, and `evidence.pm_approval`: merge, close,
   labels, tags, releases, settings, and secrets each require separate exact
   PM approval.
5. **Working-tree preflight** — checking branch, worktree, and HEAD before
   writing. Project OS: `rule.preflight`, `boundary.branch_preflight`,
   `boundary.no_main_edits`, and `evidence.branch_preflight`. The
   `npm run preflight` command in `gemini-cli` is full project validation,
   not working-tree preflight: it counts under criterion 7.
6. **Required inputs before acting** — mandatory inputs with a failure status
   when missing. Project OS: per-workflow `required_evidence` with
   `missing_status`, e.g. `evidence.issue_scope` and
   `evidence.validation_output`.
7. **Validation before delivering** — checking the change before declaring
   it ready. `claude-cookbooks`: "Quality checks" (`make check` before
   committing, notebooks top to bottom). `gemini-cli`: "Testing and Quality"
   (`npm run preflight` before PRs). `vscode-copilot-chat`: "Validating
   changes" (check compilation before declaring work complete). `codex`:
   `just fmt` and `just test` after changes, with mandatory snapshot coverage
   in UI work. Project OS: `rule.validacion_proporcional`,
   `boundary.validation_discipline`, and `evidence.validation_output`.
8. **Fail-closed** — stopping on an unresolved condition instead of guessing
   and continuing. `vscode-copilot-chat` (Partial): "Validating changes"
   forbids moving forward with compilation errors. Project OS:
   `rule.resolucion_fail_closed`, `boundary.fail_closed`, and explicit
   unresolved statuses.
9. **Review-before-close** — reviewing the work against its objective before
   declaring it done. `vscode-copilot-chat` (Partial): requires checking
   compilation output before "declaring work complete". `codex` (Partial):
   asks reviewing generated snapshots and running `just fix` before
   finalizing large changes. Project OS: `boundary.review_before_close`
   (comparing the work unit against diff, final files, validation results,
   and risks).
10. **Work traceability** — linking the change to a work unit and to a
    conventional record. `claude-cookbooks` (Partial): "Git Workflow" fixes
    branch naming and conventional commits, with no link to a work unit.
    `gemini-cli`: "Development Conventions" requires PRs linked to an
    existing issue plus Conventional Commits. Project OS:
    `rule.trazabilidad_viva` and `work/<unit>-<slug>` branches.
11. **Governance portability** — governance separable from the concrete
    repository and reusable on another target. The four conventional files
    govern their own repository by design: the convention is portable, but
    the measured content declares no reuse (Not applicable). Project OS: the
    manifest declares the model project-agnostic, the bootloader separates
    machine/adoption configuration, and adoption is copy-based by design
    (see [getting-started.md](getting-started.md)).
12. **On-demand loading** — part of the guidance is deferred to resources
    loaded only when used. `claude-cookbooks`: "Slash Commands" and the
    `.claude/` directory. `gemini-cli`: the `pr-creator` and `docs-writer`
    skills. `vscode-copilot-chat`: defers the Claude SDK documentation to an
    `AGENTS.md` in the source tree. `codex`: `codex-rs/tui/styles.md` and the
    `$remote-tests` skill. Project OS: per-tuple resolver with resolvable
    references to operations, templates, and skills. The benchmark's unit of
    measurement already excludes that on-demand context in all five stacks.
13. **Contract / live-state separation** — the durable file declares that
    live task data (issues, PRs, branches, validation results) lives outside
    and is read at task time. Project OS: `rule.estado_vivo_no_durable`,
    `boundary.no_live_state_durable`, and the separation declared in this
    benchmark's method section.

### Product conclusion

- The two stack kinds optimize different things, and the matrix shows it
  without ordering them. The four conventional files concentrate their
  observed coverage where the convention was designed to serve: technical
  knowledge of the target, validation, and on-demand loading. The Project OS
  stack concentrates its coverage on process governance — human authority per
  action, preflight, required inputs, fail-closed, review-before-close,
  traceability, and contract/live-state separation — and is Partial precisely
  on technical knowledge, which it reconstructs from live sources instead of
  inlining it.
- The governance benefit of Project OS is making explicit and verifiable what
  stays implicit or single-case in the measured files: which inputs must
  exist before acting, which actions require separate human approval, when to
  stop instead of guessing, and what to review before closing. Every Yes cell
  in its column cites a kernel key that the resolver delivers in every
  session and that the hydration tests protect.
- That governance does not depend on the project: the same contract is
  adopted by copy into another repository without rewriting it, and
  repository specifics stay in the bootloader.
- The mechanisms are complementary, not exclusive: the Project OS stack uses
  the same measured conventions (`CLAUDE.md`, `AGENTS.md`) as its shim and
  bootloader, and a project can carry its technical knowledge in those files
  next to the kernel contract. This matrix records presence in one file per
  stack at one pinned commit; it compares no complete tools and decides no
  stack choice: that depends on the project.

## Internal hydration profile

This section is an **internal profile**: it measures the Project OS kernel
against itself and compares against no third party. Its percentages are not
comparable with the main benchmark and must not be cited as savings over
conventional stacks.

Two internal references, built from the real kernel content:

- **Per-tuple baseline (the one ADR 0004 requires):** a static document
  inlining exactly what this tuple needs. It coincides with the serialized
  `full/debug` output: a static document cannot select by
  actor/workflow/mode, so it must carry the tuple's complete contract.
- **Full kernel (internal ceiling):** the byte-for-byte concatenation of the
  11 kernel JSON files, `manifest.json` first and the rest in name order:
  what inlining the entire kernel would cost to serve any tuple with no
  selection.

### Spanish kernel (default)

| Alternative | Bytes | Characters | Tokens `o200k_base` | Tokens `cl100k_base` |
| --- | ---: | ---: | ---: | ---: |
| Resolver `minimal` | 6696 | 6696 | 1646 | 1757 |
| Resolver `compact` | 15218 | 15213 | 3566 | 3885 |
| Per-tuple baseline (= `full/debug`) | 16504 | 16499 | 3939 | 4259 |
| Full kernel (11 files) | 47584 | 47579 | 11000 | 11576 |

Reduction against the per-tuple baseline: `minimal` −59.4% bytes (−58.2%
`o200k_base` tokens, −58.7% `cl100k_base`); `compact` −7.8% bytes (−9.5%,
−8.8%). Against the full kernel (internal profile only): `minimal` −85.9%
bytes (−85.0%, −84.8%); `compact` −68.0% (−67.6%, −66.4%); `full/debug`
−65.3% (−64.2%, −63.2%).

### English kernel (explicit selection)

Same tuple, same commands, with `--kernel-dir project-os-en/kernel`:

| Alternative | Bytes | Characters | Tokens `o200k_base` | Tokens `cl100k_base` |
| --- | ---: | ---: | ---: | ---: |
| Resolver `minimal` | 6509 | 6509 | 1530 | 1539 |
| Resolver `compact` | 14384 | 14384 | 3202 | 3221 |
| Per-tuple baseline (= `full/debug`) | 15670 | 15670 | 3575 | 3595 |
| Full kernel (11 files) | 46000 | 46000 | 10183 | 10200 |

Reduction against the per-tuple baseline: `minimal` −58.5% bytes; `compact`
−8.2%. Against the full kernel (internal profile only): `minimal` −85.9%
bytes; `compact` −68.7%; `full/debug` −65.9%.

### What each alternative keeps

- **`minimal`** keeps the manifest/actor/mode/workflow identity, every
  applicable boundary, prohibited actions, required inputs, allowed outputs,
  and referenced statuses: enough to stop prohibited work. It omits the full
  mandatory guidance.
- **`compact`** (the practical default) adds the mandatory operating rules,
  the selected operating context, and resolvable artifact/template/skill
  references: the view used to execute.
- **The per-tuple baseline (`full/debug`)** adds complete selected-resolution
  metadata; as a hydration level it is meant only when reviewing or auditing,
  not as the normal mode.
- **The full kernel** keeps the whole kernel, covering every tuple at once
  and selecting nothing: every session pays the full contract even when it
  needs one tuple.

The reduction drops no boundary, required input, output, status,
non-authorization, or secret-safety content: that is guarded by
`tests/test_project_os_hydration_levels.py`
(`test_levels_have_deterministic_monotonic_contract_shapes_and_keep_safety`
and
`test_requested_skills_and_existing_fail_closed_boundaries_survive_each_level`).

## Reproduction

From the repo root, with Python 3.12+:

```sh
python -m venv .venv && . .venv/bin/activate
pip install tiktoken==0.13.0

mkdir -p /tmp/pos-bench/corpus /tmp/pos-bench/stacks
curl -fsSL -o /tmp/pos-bench/corpus/claude-code-claude-cookbooks.md \
  https://raw.githubusercontent.com/anthropics/claude-cookbooks/67ce644d33e5/CLAUDE.md
curl -fsSL -o /tmp/pos-bench/corpus/gemini-cli-gemini-cli.md \
  https://raw.githubusercontent.com/google-gemini/gemini-cli/fa975395bcc6/GEMINI.md
curl -fsSL -o /tmp/pos-bench/corpus/copilot-vscode-copilot-chat.md \
  https://raw.githubusercontent.com/microsoft/vscode-copilot-chat/5863f5a70889/.github/copilot-instructions.md
curl -fsSL -o /tmp/pos-bench/corpus/codex-cli-codex.md \
  https://raw.githubusercontent.com/openai/codex/393f64565ab4/AGENTS.md

for kernel in project-os-es project-os-en; do
  for level in minimal compact full/debug; do
    python tools/project_os_resolve.py --actor actor.terminal_agent \
      --workflow workflow.issue_implementation --mode mode.delegated_commit_pr \
      --kernel-dir "$kernel/kernel" --hydration-level "$level" --compact \
      > "/tmp/pos-bench/stacks/$kernel-${level//\//-}.json"
  done
  (cd "$kernel/kernel" && cat manifest.json $(ls *.json | grep -v '^manifest')) \
    > "/tmp/pos-bench/stacks/$kernel-full-kernel.txt"
  cat CLAUDE.md AGENTS.md "/tmp/pos-bench/stacks/$kernel-compact.json" \
    > "/tmp/pos-bench/stacks/$kernel-session-stack.txt"
done

python - <<'PY'
from pathlib import Path
import tiktoken
encodings = {n: tiktoken.get_encoding(n) for n in ("o200k_base", "cl100k_base")}
for path in sorted(Path("/tmp/pos-bench").rglob("*")):
    if path.is_dir():
        continue
    text = path.read_text(encoding="utf-8")
    tokens = {name: len(enc.encode(text)) for name, enc in encodings.items()}
    print(path.name, {"bytes": len(text.encode("utf-8")), "chars": len(text), **tokens})
PY
```

`*-session-stack.txt` reproduces the Project OS rows of the main benchmark;
`/tmp/pos-bench/corpus/*` reproduces the public corpus rows;
`*-minimal.json`, `*-compact.json`, `*-full-debug.json`, and
`*-full-kernel.txt` reproduce the internal hydration profile.

## Limits of this benchmark

- The numbers hold at the declared date and commits; corpus files evolve in
  their source repositories and reproduction is only stable against the
  pinned commits. When the kernel or the corpus changes, measure again and
  update date, commits, and tables together.
- The corpus is four vendor dogfood files: verifiable and not cherry-picked
  under the declared rule, yet it represents neither every project nor every
  way of configuring each tool.
- Equivalence is functional (repo-wide instruction context loaded at session
  start given the declared task), not content-level: each corpus item governs
  a different project with different content.
- The coverage matrix records presence of instructions in concrete files at
  concrete commits; it describes no tool's complete capabilities, weighs no
  criterion, and orders no stack.
- Token counts depend on the tokenizer and the model; use your real model's
  tokenizer when planning context budgets from these figures.
- Measuring size measures neither usefulness nor quality: `minimal` is
  smaller by returning less guidance, not by always being enough. The
  practical default remains `compact` (see
  [getting-started.md](getting-started.md)).
- This document publishes no prices, costs, or subscription savings, compares
  no features, and claims no replacement of any tool.
