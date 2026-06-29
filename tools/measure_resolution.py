"""Read-only size diagnostic for Project OS kernel resolution paths.

Issue #320 asks whether the terminal resolver fast path actually reduces or
justifies context usage compared with manual manifest/kernel resolution, before
the manifest model is used as a Browser Companion packaging base (#309).

This module reports the byte / character / approximate-token size of three
resolution paths against the live kernel:

- ``manual_resolution`` — a cold manual read of ``manifest.json`` plus every
  file in ``load_order`` (what browser and non-terminal surfaces read, and what
  the fast path expands);
- ``resolver_fast_path`` — the deterministic ``tools.project_os_resolve`` output
  for one actor/workflow/mode selector, compact and pretty;
- ``browser_companion_candidate`` — the projected stable-context package a
  non-terminal Browser Companion (#309) would embed to resolve manually offline.
  This is a projection only; it creates no package and designs no #309 artifact.

It reads kernel JSON at runtime, computes sizes, compares the fast path against
the manual path and a baseline, and prints a conclusion. It writes nothing,
mutates nothing, and grants no permission (boundary.output_not_permission).

Exit codes: 0 = report produced, 2 = tooling error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from tools.project_os_resolve import resolve

# Default selector: the heaviest representative resolution (a delegated
# implementation), so the comparison reflects a real write-capable task.
DEFAULT_ACTOR = "actor.terminal_agent"
DEFAULT_WORKFLOW = "workflow.issue_implementation"
DEFAULT_MODE = "mode.delegated_commit_pr"

# PM-reported prior baseline for manual manifest/kernel resolution (~26 KB).
# Overridable so the comparison stays reproducible as the kernel evolves.
DEFAULT_BASELINE_BYTES = 26624

# Files a Browser Companion would embed for offline manual resolution: the
# surface/guardrail/mode core that is always needed before a workflow is chosen.
# Workflow/evidence/output detail can be read on demand. Projection only.
BROWSER_COMPANION_CORE = (
    "manifest.json",
    "statuses.json",
    "actors.json",
    "execution_modes.json",
    "boundaries.json",
)

NON_AUTHORIZATION = (
    "This measurement only reports sizes; it shapes nothing and grants no "
    "permission (boundary.output_not_permission)."
)


def _approx_tokens(chars: int) -> int:
    """Rough token estimate using the common ~4-characters-per-token heuristic."""
    return round(chars / 4)


def _size(text: str) -> dict[str, int]:
    """Return byte, character, and approximate-token sizes for ``text``."""
    data = text.encode("utf-8")
    return {
        "bytes": len(data),
        "chars": len(text),
        "approx_tokens": _approx_tokens(len(text)),
    }


def _load_order(kernel_dir: Path) -> list[str]:
    """Read the manifest load_order, with the manifest itself read first."""
    manifest = json.loads((kernel_dir / "manifest.json").read_text(encoding="utf-8"))
    order = manifest.get("load_order", [])
    if not isinstance(order, list):
        raise ValueError("manifest load_order is not a list")
    return ["manifest.json", *order]


def _measure_files(kernel_dir: Path, names: list[str]) -> dict[str, Any]:
    """Concatenate the named kernel files and measure the combined read."""
    files: list[dict[str, Any]] = []
    combined = ""
    for name in names:
        text = (kernel_dir / name).read_text(encoding="utf-8")
        combined += text
        files.append({"file": name, **_size(text)})
    return {**_size(combined), "files": files}


def measure(
    actor_id: str = DEFAULT_ACTOR,
    workflow_id: str = DEFAULT_WORKFLOW,
    mode_id: str = DEFAULT_MODE,
    kernel_dir: Path | str | None = None,
    baseline_bytes: int = DEFAULT_BASELINE_BYTES,
) -> dict[str, Any]:
    """Measure the resolution paths against the live kernel and conclude.

    Returns a JSON-serializable report. Reads only; never writes or authorizes.
    """
    kernel_dir = Path("kernel") if kernel_dir is None else Path(kernel_dir)

    manual = _measure_files(kernel_dir, _load_order(kernel_dir))
    companion = _measure_files(kernel_dir, list(BROWSER_COMPANION_CORE))
    companion["note"] = (
        "Projected #309 stable-context package candidate (surface/guardrail/mode "
        "core for offline manual resolution); not created here."
    )

    result = resolve(actor_id, workflow_id, mode_id, kernel_dir=kernel_dir)
    if result["status"] != "ok":
        fast_path: dict[str, Any] = {"status": "error", "errors": result["errors"]}
        comparison: dict[str, Any] = {}
        conclusion = (
            f"Selector {actor_id}/{workflow_id}/{mode_id} did not resolve; "
            f"no fast-path size to compare. Manual read is {manual['bytes']} bytes."
        )
    else:
        compact = json.dumps(result, separators=(",", ":"))
        pretty = json.dumps(result, indent=2)
        fast = _size(compact)
        fast_path = {
            "status": "ok",
            "compact_bytes": fast["bytes"],
            "compact_chars": fast["chars"],
            "compact_approx_tokens": fast["approx_tokens"],
            "pretty_bytes": len(pretty.encode("utf-8")),
        }

        manual_bytes = manual["bytes"]
        fast_bytes = fast["bytes"]
        reduction_pct = round((manual_bytes - fast_bytes) / manual_bytes * 100, 1)
        baseline_reduction_pct = (
            round((baseline_bytes - fast_bytes) / baseline_bytes * 100, 1)
            if baseline_bytes
            else None
        )
        comparison = {
            "fast_path_vs_manual_bytes_delta": fast_bytes - manual_bytes,
            "fast_path_vs_manual_reduction_pct": reduction_pct,
            "fast_path_vs_baseline_reduction_pct": baseline_reduction_pct,
        }

        if fast_bytes < manual_bytes:
            verdict = "uses less"
        elif fast_bytes == manual_bytes:
            verdict = "uses the same"
        else:
            verdict = "uses more"
        conclusion = (
            f"For one resolution, the resolver fast path output ({fast_bytes} bytes "
            f"compact) {verdict} context than a full manual kernel read "
            f"({manual_bytes} bytes): {reduction_pct}% smaller. This is a concrete "
            f"optimization on terminal surfaces only. Browser and non-terminal "
            f"surfaces cannot run the resolver; their projected stable-context "
            f"package ({companion['bytes']} bytes for the core) is the separate "
            f"concern of #309 and is unaffected by the fast path."
        )

    return {
        "kernel_dir": str(kernel_dir),
        "selector": {"actor": actor_id, "workflow": workflow_id, "mode": mode_id},
        "baseline": {
            "bytes": baseline_bytes,
            "source": "PM-reported prior manual manifest/kernel resolution (~26 KB)",
        },
        "manual_resolution": manual,
        "resolver_fast_path": fast_path,
        "browser_companion_candidate": companion,
        "comparison": comparison,
        "conclusion": conclusion,
        "non_authorization": NON_AUTHORIZATION,
    }


def _render(report: dict[str, Any]) -> str:
    """Render a compact human-readable report."""
    sel = report["selector"]
    lines = [
        "Project OS resolution size report (read-only; grants no permission)",
        f"  kernel_dir: {report['kernel_dir']}",
        f"  selector:   {sel['actor']} / {sel['workflow']} / {sel['mode']}",
        f"  baseline:   {report['baseline']['bytes']} bytes "
        f"({report['baseline']['source']})",
        "",
        f"  manual_resolution (manifest + load_order): "
        f"{report['manual_resolution']['bytes']} bytes, "
        f"~{report['manual_resolution']['approx_tokens']} tokens",
    ]
    fast = report["resolver_fast_path"]
    if fast.get("status") == "ok":
        lines.append(
            f"  resolver_fast_path (compact):              "
            f"{fast['compact_bytes']} bytes, "
            f"~{fast['compact_approx_tokens']} tokens "
            f"(pretty {fast['pretty_bytes']} bytes)"
        )
        comp = report["comparison"]
        lines.append(
            f"  fast path vs manual:  {comp['fast_path_vs_manual_reduction_pct']}% "
            f"smaller ({comp['fast_path_vs_manual_bytes_delta']} bytes)"
        )
        if comp.get("fast_path_vs_baseline_reduction_pct") is not None:
            lines.append(
                f"  fast path vs baseline: "
                f"{comp['fast_path_vs_baseline_reduction_pct']}% smaller"
            )
    else:
        lines.append(f"  resolver_fast_path: ERROR {fast.get('errors')}")
    comp_cand = report["browser_companion_candidate"]
    lines.append(
        f"  browser_companion_candidate (core, projected #309): "
        f"{comp_cand['bytes']} bytes, ~{comp_cand['approx_tokens']} tokens"
    )
    lines.append("")
    lines.append(f"  conclusion: {report['conclusion']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for the resolution size diagnostic."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--actor", default=DEFAULT_ACTOR)
    parser.add_argument("--workflow", default=DEFAULT_WORKFLOW)
    parser.add_argument("--mode", default=DEFAULT_MODE)
    parser.add_argument("--kernel-dir", default=None, help="Path to kernel/ (default: ./kernel)")
    parser.add_argument(
        "--baseline-bytes",
        type=int,
        default=DEFAULT_BASELINE_BYTES,
        help="Prior manual-resolution baseline to compare against",
    )
    parser.add_argument("--json", action="store_true", help="Emit the report as JSON")
    args = parser.parse_args(argv)

    try:
        report = measure(
            actor_id=args.actor,
            workflow_id=args.workflow,
            mode_id=args.mode,
            kernel_dir=args.kernel_dir,
            baseline_bytes=args.baseline_bytes,
        )
    except Exception as exc:  # fail closed on unexpected tooling errors
        print(f"tooling error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(report, indent=2) if args.json else _render(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
