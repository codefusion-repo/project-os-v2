"""Tests for the read-only resolution size diagnostic (issue #320).

These guard the measurement/reporting path that compares manual manifest/kernel
resolution against the terminal resolver fast path and the projected Browser
Companion (#309) stable-context package. The diagnostic reads only and grants
no permission.
"""

from __future__ import annotations

import json
from pathlib import Path

from tools.measure_resolution import BROWSER_COMPANION_CORE, main, measure

REPO_ROOT = Path(__file__).resolve().parent.parent
KERNEL_DIR = REPO_ROOT / "kernel"


class TestMeasureRealKernel:
    """The diagnostic measures the live kernel and concludes coherently."""

    def test_report_structure(self) -> None:
        report = measure(kernel_dir=KERNEL_DIR)
        assert set(report) == {
            "kernel_dir",
            "selector",
            "baseline",
            "manual_resolution",
            "resolver_fast_path",
            "browser_companion_candidate",
            "comparison",
            "conclusion",
            "non_authorization",
        }

    def test_fast_path_smaller_than_manual(self) -> None:
        report = measure(kernel_dir=KERNEL_DIR)
        fast = report["resolver_fast_path"]
        assert fast["status"] == "ok"
        assert fast["compact_bytes"] < report["manual_resolution"]["bytes"]
        assert report["comparison"]["fast_path_vs_manual_reduction_pct"] > 0
        assert "uses less" in report["conclusion"]

    def test_sizes_report_bytes_chars_and_tokens(self) -> None:
        report = measure(kernel_dir=KERNEL_DIR)
        manual = report["manual_resolution"]
        for key in ("bytes", "chars", "approx_tokens"):
            assert isinstance(manual[key], int) and manual[key] > 0
        # The token estimate uses the documented ~4-chars-per-token heuristic.
        assert manual["approx_tokens"] == round(manual["chars"] / 4)

    def test_manual_path_equals_manifest_plus_load_order(self) -> None:
        report = measure(kernel_dir=KERNEL_DIR)
        names = [entry["file"] for entry in report["manual_resolution"]["files"]]
        assert names[0] == "manifest.json"
        combined = "".join(
            (KERNEL_DIR / name).read_text(encoding="utf-8") for name in names
        )
        assert report["manual_resolution"]["bytes"] == len(combined.encode("utf-8"))

    def test_browser_companion_candidate_is_a_projection(self) -> None:
        report = measure(kernel_dir=KERNEL_DIR)
        candidate = report["browser_companion_candidate"]
        assert candidate["bytes"] > 0
        # The core is a subset of the full manual read.
        assert candidate["bytes"] <= report["manual_resolution"]["bytes"]
        assert {entry["file"] for entry in candidate["files"]} == set(BROWSER_COMPANION_CORE)
        assert "not created here" in candidate["note"]

    def test_baseline_comparison_present(self) -> None:
        report = measure(kernel_dir=KERNEL_DIR)
        assert report["baseline"]["bytes"] > 0
        assert report["comparison"]["fast_path_vs_baseline_reduction_pct"] is not None

    def test_output_is_non_authorizing(self) -> None:
        report = measure(kernel_dir=KERNEL_DIR)
        assert "boundary.output_not_permission" in report["non_authorization"]
        assert "grants no permission" in report["non_authorization"]


class TestUnresolvableSelector:
    """A selector that does not resolve is handled without crashing."""

    def test_unresolvable_selector_reports_manual_only(self) -> None:
        # human_pm has no agent modes, so the resolver returns an error; every id
        # here is real, so the kernel-id reference guard stays satisfied.
        report = measure(
            actor_id="actor.human_pm",
            workflow_id="workflow.issue_implementation",
            mode_id="mode.delegated_commit_pr",
            kernel_dir=KERNEL_DIR,
        )
        assert report["resolver_fast_path"]["status"] == "error"
        assert report["comparison"] == {}
        assert "did not resolve" in report["conclusion"]
        assert report["manual_resolution"]["bytes"] > 0


class TestCLI:
    """The CLI prints both human-readable and JSON reports and exits 0."""

    def test_main_human_readable(self, capsys) -> None:
        code = main(["--kernel-dir", str(KERNEL_DIR)])
        assert code == 0
        out = capsys.readouterr().out
        assert "resolution size report" in out
        assert "conclusion:" in out

    def test_main_json(self, capsys) -> None:
        code = main(["--kernel-dir", str(KERNEL_DIR), "--json"])
        assert code == 0
        report = json.loads(capsys.readouterr().out)
        assert report["resolver_fast_path"]["status"] == "ok"

    def test_main_custom_baseline(self, capsys) -> None:
        code = main(["--kernel-dir", str(KERNEL_DIR), "--baseline-bytes", "1", "--json"])
        assert code == 0
        report = json.loads(capsys.readouterr().out)
        assert report["baseline"]["bytes"] == 1
