# Reproducible context benchmark

**How much context a kernel resolution consumes at each hydration level,
compared with a monolithic baseline built from the real kernel content.** This
benchmark only reports sizes: it does not measure quality, it promises no
universal savings, and it grants no permission
(`boundary.output_not_permission`).

Spanish version: [benchmark-contexto.md](../../project-os-es/docs/benchmark-contexto.md).

## Declared method

- **Measurement date:** 2026-07-14.
- **Tree state:** commit `b9f8805` of `codefusion-repo/project-os-v2` (the
  `project-os-es/kernel/` and `project-os-en/kernel/` directories did not
  change on the branch that added this document).
- **Measured tuple (identical across every alternative):**
  `actor.terminal_agent` / `workflow.issue_implementation` /
  `mode.delegated_commit_pr`.
- **Corpus:** the exact resolver CLI stdout with `--compact` (single-line
  JSON, trailing newline included) at each hydration level, plus a monolithic
  baseline: the byte-for-byte concatenation of the 11 kernel JSON files,
  `manifest.json` first and the rest in name order. The baseline represents
  what an `AGENTS.md`-style bootloader would have to inline to serve any tuple
  without selection: a static document cannot select by actor/workflow/mode,
  which is exactly what the resolver does.
- **Metrics:** UTF-8 bytes, characters, and tokens.
- **Declared tokenizer:** `tiktoken` 0.13.0 (Python 3.12.13), with two public
  encodings to show cross-tokenizer variation: `o200k_base` and `cl100k_base`.
  Token counts depend on the tokenizer and the model: no number in these
  tables is a universal saving.
- **Selected kernel vs live project data:** resolver output contains only
  already-resolved kernel contract. It includes no issues, PRs, branches,
  diffs, or any other live project data — that is read from GitHub at task
  time and stays outside this measurement by design.

## Results — Spanish kernel (default)

| Alternative | Bytes | Characters | Tokens `o200k_base` | Tokens `cl100k_base` |
| --- | ---: | ---: | ---: | ---: |
| Resolver `minimal` | 6696 | 6696 | 1646 | 1757 |
| Resolver `compact` | 15218 | 15213 | 3566 | 3885 |
| Resolver `full/debug` | 16504 | 16499 | 3939 | 4259 |
| Monolithic baseline (11 kernel files) | 47584 | 47579 | 11000 | 11576 |

Reduction against the baseline: `minimal` −85.9% bytes (−85.0% `o200k_base`
tokens, −84.8% `cl100k_base`); `compact` −68.0% bytes (−67.6%, −66.4%);
`full/debug` −65.3% bytes (−64.2%, −63.2%).

## Results — English kernel (explicit selection)

Same tuple, same commands, with `--kernel-dir project-os-en/kernel`:

| Alternative | Bytes | Characters | Tokens `o200k_base` | Tokens `cl100k_base` |
| --- | ---: | ---: | ---: | ---: |
| Resolver `minimal` | 6509 | 6509 | 1530 | 1539 |
| Resolver `compact` | 14384 | 14384 | 3202 | 3221 |
| Resolver `full/debug` | 15670 | 15670 | 3575 | 3595 |
| Monolithic baseline (11 kernel files) | 46000 | 46000 | 10183 | 10200 |

Reduction against the baseline: `minimal` −85.9% bytes; `compact` −68.7%;
`full/debug` −65.9%.

## What each alternative keeps

- **`minimal`** keeps the manifest/actor/mode/workflow identity, every
  applicable boundary, prohibited actions, required evidence, allowed outputs,
  and referenced statuses: enough to stop prohibited work. It omits the full
  mandatory guidance.
- **`compact`** (the practical default) adds the mandatory operating rules,
  the selected operating context, and resolvable artifact/template/skill
  references: the view used to execute.
- **`full/debug`** adds complete selected-resolution metadata; it is meant
  only when reviewing or auditing, not as the normal mode.
- **The monolithic baseline** keeps the whole kernel, covering every tuple at
  once and selecting nothing: every session pays the full contract even when
  it needs one tuple.

The reduction drops no boundary, evidence, output, status,
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
for level in minimal compact full/debug; do
  python tools/project_os_resolve.py --actor actor.terminal_agent \
    --workflow workflow.issue_implementation --mode mode.delegated_commit_pr \
    --kernel-dir project-os-es/kernel --hydration-level "$level" --compact \
    > "/tmp/pos-bench/${level//\//-}.json"
done
(cd project-os-es/kernel && cat manifest.json $(ls *.json | grep -v '^manifest')) \
  > /tmp/pos-bench/baseline.txt

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

To measure the English kernel, repeat the same commands replacing
`project-os-es/kernel` with `project-os-en/kernel`.

## Limits of this benchmark

- The numbers hold at the declared date and commit; when the kernel changes,
  re-run the reproduction and update date, commit, and tables together.
- Token counts depend on the tokenizer and the model; use your real model's
  tokenizer when planning context budgets from these figures.
- Measuring size does not measure usefulness: `minimal` is smaller by
  returning less guidance, not by always being enough. The practical default
  remains `compact` (see [getting-started.md](getting-started.md)).
- This document publishes no prices, costs, or subscription savings and
  compares no providers.
