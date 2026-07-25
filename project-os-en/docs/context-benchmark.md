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

- **Measurement date:** 2026-07-25.
- **Inputs:** commit `5afb2c7` of `codefusion-repo/project-os-v2`; the
  measured inputs (both kernel directories and
  `tools/project_os_resolve.py`) do not change after that commit on the
  branch updating this document.
- **Constant change class:** `change_class.small` at all three levels, with the
  level selected explicitly through `--hydration-level`. Since #462 a mutating
  workflow requires a declared class, and the class is material: it contributes
  its own `change_class` block, its `remaining_gates`, and its default density.
  Varying the class alongside the level would mix two effects, so here the
  class stays fixed and only hydration changes. The resolver allows this
  because an explicit level may keep or raise a class's contractual density; it
  only blocks lowering it.
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
| Resolver `minimal` | 16760 | 16760 | 3956 | 4139 |
| Resolver `compact` | 33760 | 33713 | 7612 | 8251 |
| Per-tuple baseline (= `full/debug`) | 38250 | 38203 | 8716 | 9389 |
| Full kernel (11 files) | 78981 | 78934 | 17756 | 18728 |

Reduction against the per-tuple baseline: `minimal` −56.2% bytes (−54.6%
`o200k_base` tokens, −55.9% `cl100k_base`); `compact` −11.7% bytes (−12.7%,
−12.1%). Against the full kernel (internal profile only): `minimal` −78.8%
bytes (−77.7%, −77.9%); `compact` −57.3% (−57.1%, −55.9%); `full/debug`
−51.6% (−50.9%, −49.9%).

## English kernel (explicit selection)

Same tuple, same commands, with `--kernel-dir project-os-en/kernel`:

| Alternative | Bytes | Characters | Tokens `o200k_base` | Tokens `cl100k_base` |
| --- | ---: | ---: | ---: | ---: |
| Resolver `minimal` | 16446 | 16446 | 3752 | 3741 |
| Resolver `compact` | 32592 | 32592 | 6988 | 6983 |
| Per-tuple baseline (= `full/debug`) | 37051 | 37051 | 8061 | 8057 |
| Full kernel (11 files) | 76958 | 76958 | 16583 | 16560 |

Reduction against the per-tuple baseline: `minimal` −55.6% bytes; `compact`
−12.0%. Against the full kernel (internal profile only): `minimal` −78.6%
bytes; `compact` −57.7%; `full/debug` −51.9%.

## Source-receipt cost (#464)

Before #464 every resolution carried the complete receipt contract plus a
`context_plan` that repeated part of it, at all three levels. This section
compares the **immediate baseline** `3de282f` against the corrected #464 state,
running exactly the same command on both: same tuple, same `change_class.small`,
and the same explicit `--hydration-level`.

Complete resolution, Spanish kernel, UTF-8 bytes:

| Level | `3de282f` | With #464 | Δ bytes | Δ % |
| --- | ---: | ---: | ---: | ---: |
| `minimal` | 19332 | 16760 | −2572 | −13.3% |
| `compact` | 36211 | 33760 | −2451 | −6.8% |
| `full/debug` | 40712 | 38250 | −2462 | −6.0% |

Complete resolution, English kernel, UTF-8 bytes:

| Level | `3de282f` | With #464 | Δ bytes | Δ % |
| --- | ---: | ---: | ---: | ---: |
| `minimal` | 19008 | 16446 | −2562 | −13.5% |
| `compact` | 35063 | 32592 | −2471 | −7.0% |
| `full/debug` | 39533 | 37051 | −2482 | −6.3% |

Nearly all of that difference comes from the receipt. Measuring the two
surfaces separately inside the same resolution — each subobject reserialized
with `json.dumps(obj, ensure_ascii=False)`, the same format the resolver emits
its output with, and counted in UTF-8 bytes — the receipt cost per resolution
is:

| Surface | Before (ES) | Before (EN) | After |
| --- | ---: | ---: | ---: |
| `context_receipt_contract` | 1300 | 1300 | 921 |
| `context_plan` on the normal route | 2175–2265 | 2165–2255 | 0 |
| Total receipt cost per resolution | 3475–3565 | 3465–3555 | 921 |

The ranges cover the three levels: the receipt contract does not vary with
hydration, and the former `context_plan` grew from `minimal` to `full/debug`.

Because the format matches the output's, these figures are additive against the
totals. At `minimal` the receipt accounts for the whole difference: −2554 bytes
of content plus the 18 of the dropped `context_plan` key give exactly the −2572
of the previous table (−2544 + 18 = −2562 on the English kernel). At `compact`
and `full/debug` the receipt reduction exceeds the net one because #464 also
added prose to the operating rules — 200 bytes in Spanish and 170 in English —
which are carried only from `compact` up. The balance stays negative in all six
measured cases.

Detailed provenance remains available outside the normal route with
`--context-provenance <reason>`, and that cost is no longer paid on every
resolution.

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

To reproduce the #464 comparison, run that same loop in a baseline worktree and
compare again:

```sh
git worktree add /tmp/pos-base 3de282f07c65f8751d6827dd941dba7cbf90ef86 --detach
```

And for the per-surface breakdown, on either state:

```sh
python - <<'PY'
import json, subprocess, sys
for level in ("minimal", "compact", "full/debug"):
    out = subprocess.run([sys.executable, "tools/project_os_resolve.py",
        "--actor", "actor.terminal_agent",
        "--workflow", "workflow.issue_implementation",
        "--mode", "mode.delegated_commit_pr",
        "--change-class", "change_class.small",
        "--hydration-level", level,
        "--kernel-dir", "project-os-es/kernel", "--compact"],
        capture_output=True, text=True, check=True).stdout
    payload = json.loads(out)
    def size(obj):
        if obj is None:
            return 0
        return len(json.dumps(obj, ensure_ascii=False).encode("utf-8"))
    print(level,
          "receipt", size(payload["resuelto"]["workflow"].get("context_receipt_contract")),
          "plan", size(payload.get("context_plan")),
          "total", len(out.encode("utf-8")))
PY
```

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
