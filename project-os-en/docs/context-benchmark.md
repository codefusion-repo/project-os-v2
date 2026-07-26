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

- **Measurement date:** 2026-07-26.
- **Inputs:** commit `3a52509` of
  `codefusion-repo/project-os-v2`; the
  measured inputs (both kernel directories and
  `tools/project_os_resolve.py`) do not change after that commit on the
  branch updating this document.
- **Constant change class:** `change_class.small` at all three levels, with the
  level selected explicitly through `--hydration-level`. Since #462 a mutating
  workflow requires a declared class, and the class is material: it contributes
  its own `change_class` block and its `remaining_gates`.
  Varying the class alongside the level would mix two effects, so here the
  class stays fixed and only hydration changes. Since #468 all three levels are
  available for every class: the class governs the material gates and the
  report density, never hydration.
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
| Resolver `minimal` | 15746 | 15746 | 3728 | 3920 |
| Resolver `compact` | 32897 | 32850 | 7413 | 8074 |
| Per-tuple baseline (= `full/debug`) | 36783 | 36736 | 8389 | 9068 |
| Full kernel (11 files) | 77199 | 77152 | 17355 | 18367 |

Reduction against the per-tuple baseline: `minimal` −57.2% bytes (−55.6%
`o200k_base` tokens, −56.8% `cl100k_base`); `compact` −10.6% bytes (−11.6%,
−11.0%). Against the full kernel (internal profile only): `minimal` −79.6%
bytes (−78.5%, −78.7%); `compact` −57.4% (−57.3%, −56.0%); `full/debug`
−52.4% (−51.7%, −50.6%).

## English kernel (explicit selection)

Same tuple, same commands, with `--kernel-dir project-os-en/kernel`:

| Alternative | Bytes | Characters | Tokens `o200k_base` | Tokens `cl100k_base` |
| --- | ---: | ---: | ---: | ---: |
| Resolver `minimal` | 15421 | 15421 | 3521 | 3517 |
| Resolver `compact` | 31700 | 31700 | 6789 | 6790 |
| Per-tuple baseline (= `full/debug`) | 35578 | 35578 | 7755 | 7757 |
| Full kernel (11 files) | 75154 | 75154 | 16182 | 16185 |

Reduction against the per-tuple baseline: `minimal` −56.7% bytes; `compact`
−10.9%. Against the full kernel (internal profile only): `minimal` −79.5%
bytes; `compact` −57.8%; `full/debug` −52.7%.

## Normal critical case (#468)

Until #468 the class selected hydration: a `change_class.critical` resolution
without an override automatically received `full/debug`. Since #468 the global
default is `compact` for every class. This section measures that concrete case
on the same final state, with the class fixed, so hydration is the only
variable:

| Kernel | Before (automatic `full/debug`) | After (default `compact`) | Δ bytes | Δ % |
| --- | ---: | ---: | ---: | ---: |
| Spanish | 37384 | 33498 | −3886 | −10.4% |
| English | 36156 | 32278 | −3878 | −10.7% |

In tokens: Spanish 8518 → 7542 `o200k_base` (−11.5%) and 9216 → 8222
`cl100k_base` (−10.8%); English 7865 → 6899 (−12.3%) and 7868 → 6901 (−12.3%).

The "before" row reproduces exactly the projection the class used to activate
automatically, by running `--change-class change_class.critical
--hydration-level full/debug` today; the "after" row runs the same command
without `--hydration-level`. Measuring both on the final state isolates the
hydration effect from kernel growth, which this document never adds together.

What does **not** change between those two rows, verified in the same
resolution: `formal_unit_required=true`, `pr_required=true`,
`review_level=review.independent`, `validation_level=validation.broad`,
`prior_docs=expected`, and an `output.execution_report` carrying the 10
`must_include` fields of the `full/debug` density. The reduction is serialized
contract, not gates and not report density.

This measurement separates two costs that used to be conflated:

- **hydration cost:** the table's difference, the only effect of #468;
- **the agent's external reads:** outside resolver output and therefore outside
  this measurement. No level requires re-reading the kernel the resolver
  already processed, so a manual re-read is not attributable to the level.

## Complete removal of the receipt and provenance structure (#477), and residual guidance correction (#479)

The structural-removal measurement compares the immediately preceding `main`
baseline, commit `4a22ce3`, with implementation commit `9553b1c`. Both sides
run the same tuple, `change_class.small`, explicit levels, and `--compact` JSON.

| Kernel | Level | Before (UTF-8 bytes) | After (UTF-8 bytes) | Δ bytes | Δ % |
| --- | --- | ---: | ---: | ---: | ---: |
| ES | `minimal` | 16823 | 15746 | −1077 | −6.4% |
| ES | `compact` | 34180 | 33103 | −1077 | −3.2% |
| ES | `full/debug` | 38066 | 36989 | −1077 | −2.8% |
| EN | `minimal` | 16498 | 15421 | −1077 | −6.5% |
| EN | `compact` | 32962 | 31885 | −1077 | −3.3% |
| EN | `full/debug` | 36840 | 35763 | −1077 | −2.9% |

The identifiers in this list appear only as historical names for the removed
baseline structure: `context_receipt_contract`, `context_receipt_key`,
`context_plan`, `context_provenance`, `executor_reported_fields`, and
`--context-provenance`. The after state serializes and exposes none of them;
there is no functional replacement.

The comparison verifies that limits, prohibited actions, required evidence,
allowed outputs, statuses, change-class gates, and report density remain present
and equivalent at every level. The reduction is retired structure, not omitted
live evidence: `Reviewed evidence`, validation, risks, safe degradation, exact
authorization, secret safety, and fail-closed remain in their real contracts.

The #479 residual-guidance correction measures input baseline `9553b1c` against
final input commit `3a52509`. `minimal` is
unchanged because it does not project operating rules; `compact` and
`full/debug` incorporate the corrected rule. This independent reduction is not
attributed to #477's structural removal.

| Kernel | Level | Before (UTF-8 bytes) | After (UTF-8 bytes) | Δ bytes | Δ % |
| --- | --- | ---: | ---: | ---: | ---: |
| ES | `minimal` | 15746 | 15746 | 0 | 0.0% |
| ES | `compact` | 33103 | 32897 | −206 | −0.6% |
| ES | `full/debug` | 36989 | 36783 | −206 | −0.6% |
| EN | `minimal` | 15421 | 15421 | 0 | 0.0% |
| EN | `compact` | 31885 | 31700 | −185 | −0.6% |
| EN | `full/debug` | 35763 | 35578 | −185 | −0.5% |

## Comparability with earlier measurements

The measurement published on 2026-07-18 over `7a7aab5` is **not directly
comparable** with the tables above: it precedes the change-class contract
introduced by #462 and PR #463, so its resolution carried neither the
`change_class` block, nor its `remaining_gates`, nor the workflow's
`proportionality_contract`, and it did not require declaring a class either.

Between `7a7aab5` and `3de282f` the full kernel grew from 67020 to 79302 bytes
in Spanish (+18.3%) and from 65285 to 77309 in English (+18.4%). That
**accumulated kernel growth** — not #464 — is why the resolver rows are larger
than on July 18. #464's own contribution, measured against its immediate
baseline with the class held constant, is a **reduction** at all three levels
and on both kernels. These are two distinct effects and this document does not
add them together.

## What each alternative keeps

- **`minimal`** keeps the manifest/actor/mode/workflow identity, every
  applicable boundary, prohibited actions, required inputs, allowed outputs,
  and referenced statuses: enough to stop prohibited work. It omits the full
  mandatory guidance.
- **`compact`** (the practical default) adds the mandatory operating rules,
  the selected operating context, and resolvable artifact/template/skill
  references: the view used to execute.
- **The per-tuple baseline (`full/debug`)** adds complete selected-resolution
  metadata; as a hydration level it is an opt-in for auditing the kernel or
  debugging the resolver, never the normal mode and never a consequence of the
  class.
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
      --change-class change_class.small --hydration-level "$level" \
      --kernel-dir "$kernel/kernel" --compact \
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

To reproduce the normal critical case from #468, on the final state and with no
extra worktree:

```sh
for kernel in project-os-es project-os-en; do
  python tools/project_os_resolve.py --actor actor.terminal_agent \
    --workflow workflow.issue_implementation --mode mode.delegated_commit_pr \
    --change-class change_class.critical --hydration-level full/debug \
    --kernel-dir "$kernel/kernel" --compact | wc -c
  python tools/project_os_resolve.py --actor actor.terminal_agent \
    --workflow workflow.issue_implementation --mode mode.delegated_commit_pr \
    --change-class change_class.critical \
    --kernel-dir "$kernel/kernel" --compact | wc -c
done
```

The second invocation of each pair declares `"hydration_level": "compact"` and
keeps the same `remaining_gates` and the same 10-field `must_include` as the
first; `jq '.hydration_level, .resuelto.change_class.remaining_gates'` verifies
it without re-reading the kernel.

To reproduce the #477 removal measurement, in a checkout where those commits
are available:

```sh
git worktree add --detach /tmp/pos-477-before 4a22ce3
git worktree add --detach /tmp/pos-477-after 9553b1c

python - /tmp/pos-477-before /tmp/pos-477-after <<'PY'
import json
import subprocess
import sys
from pathlib import Path

before, after = map(Path, sys.argv[1:])
levels = ("minimal", "compact", "full/debug")
kernels = ("project-os-es", "project-os-en")
retired = (
    "context_receipt", "context_plan", "context_provenance",
    "executor_reported_fields", "detailed_provenance_reasons",
)

def resolve(root, kernel, level):
    return subprocess.run([
        sys.executable, "tools/project_os_resolve.py",
        "--actor", "actor.terminal_agent",
        "--workflow", "workflow.issue_implementation",
        "--mode", "mode.delegated_commit_pr",
        "--change-class", "change_class.small",
        "--hydration-level", level,
        "--kernel-dir", f"{kernel}/kernel", "--compact",
    ], cwd=root, check=True, capture_output=True, text=True).stdout

def normalize(value):
    if isinstance(value, dict):
        return {
            key: normalize(item) for key, item in value.items()
            if key not in {"context_receipt_key", "context_receipt_contract"}
        }
    if isinstance(value, list):
        return [normalize(item) for item in value]
    return value

for kernel in kernels:
    for level in levels:
        old, new = resolve(before, kernel, level), resolve(after, kernel, level)
        old_payload, new_payload = json.loads(old), json.loads(new)
        assert len(new.encode("utf-8")) <= len(old.encode("utf-8"))
        assert not any(name in new for name in retired)
        for field in ("limites", "estados_permitidos"):
            assert old_payload["resuelto"][field] == new_payload["resuelto"][field]
        for field in ("required_evidence", "minimum_evidence", "allowed_outputs"):
            assert normalize(old_payload["resuelto"]["workflow"][field]) == new_payload["resuelto"]["workflow"][field]
        assert old_payload["resuelto"]["change_class"] == new_payload["resuelto"]["change_class"]
        print(kernel, level, len(old.encode("utf-8")), len(new.encode("utf-8")))
PY
```

To reproduce the #479 guidance correction, reuse the same script with the
declared baseline and final input commit:

```sh
git worktree add --detach /tmp/pos-479-before 9553b1c
git worktree add --detach /tmp/pos-479-after 3a52509
```

Run the #477 Python block above again verbatim, replacing its two arguments
with `/tmp/pos-479-before` and `/tmp/pos-479-after`.

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
  global default remains `compact` (see
  [getting-started.md](getting-started.md)).
- The critical-case reduction is serialized contract and touches no gate,
  authority, or report density; it also does not cover manual re-reads.
- This document publishes no prices, costs, or subscription savings, compares
  no features, and claims no replacement of any tool.
