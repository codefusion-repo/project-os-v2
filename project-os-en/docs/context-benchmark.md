# Reproducible context benchmark

**How much instruction context an agent session loads at start, measured over
real, publicly verifiable conventional stacks and over the Project OS stack,
against one declared task.** This benchmark only reports sizes: it does not
measure quality, it does not demonstrate savings against any stack, it
promises no universal savings, and it grants no permission
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
- Token counts depend on the tokenizer and the model; use your real model's
  tokenizer when planning context budgets from these figures.
- Measuring size measures neither usefulness nor quality: `minimal` is
  smaller by returning less guidance, not by always being enough. The
  practical default remains `compact` (see
  [getting-started.md](getting-started.md)).
- This document publishes no prices, costs, or subscription savings, compares
  no features, and claims no replacement of any tool.
