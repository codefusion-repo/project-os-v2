"""CLI guards for resolution measurement against the active Spanish kernel."""

from __future__ import annotations

import json
from pathlib import Path

from dogfooding.tools.measure_resolution import main, measure


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_measure_uses_active_spanish_kernel_and_marks_candidate_non_active() -> None:
    report = measure(kernel_dir=REPO_ROOT / "project-os-es/kernel")

    assert report["resolver_fast_path"]["status"] == "ok"
    assert report["kernel_dir"].endswith("project-os-es/kernel")
    assert "not created here" in report["browser_companion_candidate"]["note"]
    assert "grants no permission" in report["non_authorization"]
    assert "legacy" not in report["conclusion"].lower()


def test_measure_cli_json_and_human_outputs(capsys) -> None:
    assert main(["--kernel-dir", "project-os-es/kernel", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["resolver_fast_path"]["status"] == "ok"

    assert main(["--kernel-dir", "project-os-es/kernel"]) == 0
    human = capsys.readouterr().out
    assert "Project OS resolution size report" in human
    assert "project-os-es/kernel" in human
    assert "grants no permission" in human
