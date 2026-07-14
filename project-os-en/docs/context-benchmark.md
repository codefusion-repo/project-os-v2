# Reproducible internal hydration profile

**How much already-resolved contract the Project OS resolver returns at each
hydration level, measured against two internal references built from the real
kernel, at one declared tuple.** This is the reproducible context benchmark
ADR 0004 requires
([0004-public-presentation-and-packaging.md](../../docs/decisions/0004-public-presentation-and-packaging.md))
and it is an **internal profile**: it measures the Project OS kernel against
itself and compares against no external tool. It measures no quality, it
neither demonstrates nor promises any saving outside this profile, and it
grants no permission (`boundary.output_not_permission`).

This document is the technical appendix of [benefits.md](benefits.md), which
holds the explanation of benefits, the modular architecture, and Project OS's
own scenarios.

Spanish version: [benchmark-contexto.md](../../project-os-es/docs/benchmark-contexto.md).

## Declared task and unit of measurement

- **Declared task:** govern a terminal coding agent implementing a scoped
  work unit inside a repository.
- **Measured tuple:** `actor.terminal_agent` / `workflow.issue_implementation`
  / `mode.delegated_commit_pr`, identical across every alternative.
- **Unit of measurement:** resolver stdout at that tuple per hydration
  level, with `--compact` (unindented JSON), plus the two internal references
  described below. On-demand context (MOS operations, templates, skills)
  stays out: it loads only when used.

## Declared method

- **Measurement date:** 2026-07-14.
- **Inputs:** commit `84a615d2b838` of `codefusion-repo/project-os-v2`; the
  measured inputs (both kernel directories and
  `tools/project_os_resolve.py`) do not change after that commit on the
  branch correcting this document.
- **Metrics:** UTF-8 bytes, characters, and tokens.
- **Declared tokenizer:** `tiktoken` 0.13.0 (Python 3.12.13), with two public
  encodings to show cross-tokenizer variation: `o200k_base` and `cl100k_base`.
  Token counts depend on the tokenizer and the model: no number in these
  tables is a universal saving.
- **Selected kernel vs live project data:** resolver output contains only
  already-resolved kernel contract. It includes no issues, PRs, branches,
  diffs, or any other live project data — that is read from GitHub at task
  time and stays outside this measurement by design.

## Internal references

Two references, built from the real kernel content:

- **Per-tuple baseline (the one ADR 0004 requires):** a static document
  inlining exactly what this tuple needs. It coincides with the serialized
  `full/debug` output: a static document cannot select by
  actor/workflow/mode, so it must carry the tuple's complete contract.
- **Full kernel (internal ceiling):** the byte-for-byte concatenation of the
  11 kernel JSON files, `manifest.json` first and the rest in name order:
  what inlining the entire kernel would cost to serve any tuple with no
  selection.

## Spanish kernel (default)

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

## English kernel (explicit selection)

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

## What each alternative keeps

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

mkdir -p /tmp/pos-bench
for kernel in project-os-es project-os-en; do
  for level in minimal compact full/debug; do
    python tools/project_os_resolve.py --actor actor.terminal_agent \
      --workflow workflow.issue_implementation --mode mode.delegated_commit_pr \
      --kernel-dir "$kernel/kernel" --hydration-level "$level" --compact \
      > "/tmp/pos-bench/$kernel-${level//\//-}.json"
  done
  (cd "$kernel/kernel" && cat manifest.json $(ls *.json | grep -v '^manifest')) \
    > "/tmp/pos-bench/$kernel-full-kernel.txt"
done

python - <<'PY'
from pathlib import Path
import tiktoken
encodings = {n: tiktoken.get_encoding(n) for n in ("o200k_base", "cl100k_base")}
for path in sorted(Path("/tmp/pos-bench").iterdir()):
    text = path.read_text(encoding="utf-8")
    tokens = {name: len(enc.encode(text)) for name, enc in encodings.items()}
    print(path.name, {"bytes": len(text.encode("utf-8")), "chars": len(text), **tokens})
PY
```

`*-minimal.json`, `*-compact.json`, and `*-full-debug.json` reproduce the
resolver rows; `*-full-kernel.txt` reproduces the full-kernel row. The
per-tuple baseline is the same `*-full-debug.json` (see "Internal
references").

## Limits of this profile

- The numbers hold at the declared date and commit. When the kernel or the
  resolver changes, measure again and update date, commit, and tables
  together.
- This is an internal profile: its percentages compare the kernel's own
  hydration levels with each other and **must not be cited as savings over
  any external tool, convention, or stack**.
- Token counts depend on the tokenizer and the model; use your real model's
  tokenizer when planning context budgets from these figures.
- Measuring size measures neither usefulness nor quality: `minimal` is
  smaller by returning less guidance, not by always being enough. The
  practical default remains `compact` (see
  [getting-started.md](getting-started.md)).
- This document publishes no prices, costs, or subscription savings, compares
  no features, and claims no replacement of any tool.
