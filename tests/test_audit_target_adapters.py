"""Tests for the read-only target-adapter auditor."""

from __future__ import annotations

import io
import json
import subprocess
import textwrap
from pathlib import Path

import pytest

from tools.audit_target_adapters import Finding, Source, audit_target_adapters, main

REPO = "acme/widgets"
PROJECT = "widgets"
ROADMAP = "#274"


def codes(findings: list[Finding]) -> set[str]:
    return {finding.code for finding in findings}


def adapter_text(
    target: Path,
    *,
    version: str = "tracks latest",
    repo: str = REPO,
    roadmap: str = ROADMAP,
    repository_local_path: str | None = None,
    kernel_local_path: str | None = None,
    notes: str = "Run `python3 -m pytest` for local validation.",
    extra: str = "",
) -> str:
    repository_local_path = repository_local_path or str(target.resolve())
    kernel_local_path = kernel_local_path or f"{target.resolve()}/../project-os-v2/kernel"
    return textwrap.dedent(
        f"""\
        # AGENTS.md

        ## Contract

        AGENTS.md is the repository-wide terminal-agent adapter and bootloader for
        `{repo}`.

        This file is not the source of truth. The project-os-v2-min kernel is the
        source of truth for generic operating behavior.

        ## Repository identity

        PROJECT_NAME = {PROJECT}
        REPOSITORY_NAME = {repo}
        REPOSITORY_LOCAL_PATH = {repository_local_path}
        DEFAULT_BRANCH = main
        WORK_BRANCH_PATTERN = work/*
        PM_FACING_LANGUAGE = es
        KERNEL_REPOSITORY = codefusion-repo/project-os-v2
        KERNEL_LOCAL_PATH = {kernel_local_path}
        KERNEL_VERSION_ADOPTED = {version}

        ## Kernel resolution

        Before non-trivial work, resolve behavior from the kernel.

        ## Live state

        Reconstruct project state from GitHub and git at task time: current issue,
        linked PRs, the canonical roadmap issue {roadmap}, and ADRs when present.

        ## Project-specific notes

        {notes}
        {extra}
        """
    )


def browser_text(target: Path, *, version: str = "tracks latest", repo: str = REPO, roadmap: str = ROADMAP) -> str:
    return adapter_text(target, version=version, repo=repo, roadmap=roadmap).replace("# AGENTS.md", "# BROWSER_CHAT.md", 1)


def write_target(
    tmp_path: Path,
    *,
    version: str = "tracks latest",
    repo: str = REPO,
    roadmap: str = ROADMAP,
    repository_local_path: str | None = None,
    kernel_local_path: str | None = None,
    notes: str = "Run `python3 -m pytest` for local validation.",
    extra: str = "",
    claude: bool = True,
) -> Path:
    target = tmp_path / "target"
    target.mkdir()
    (target / "AGENTS.md").write_text(
        adapter_text(
            target,
            version=version,
            repo=repo,
            roadmap=roadmap,
            repository_local_path=repository_local_path,
            kernel_local_path=kernel_local_path,
            notes=notes,
            extra=extra,
        ),
        encoding="utf-8",
    )
    if claude:
        (target / "CLAUDE.md").write_text(
            textwrap.dedent(
                f"""\
                # CLAUDE.md

                CLAUDE.md is the Claude-specific adapter for `{repo}`. It is a compact
                bootloader only.

                Use `AGENTS.md` for repository-wide terminal-agent behavior. Resolve generic
                operating behavior from the project-os-v2-min kernel referenced there
                (`KERNEL_LOCAL_PATH`), and live project state from GitHub and git at task time.
                """
            ),
            encoding="utf-8",
        )
    return target


def run_git(target: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=target, check=True, capture_output=True, text=True)


def test_valid_rolling_adapter_passes(tmp_path: Path) -> None:
    target = write_target(tmp_path, version="tracks latest")
    findings = audit_target_adapters(target, REPO, browser_chat=Source("BROWSER_CHAT.md", browser_text(target)))
    assert findings == []


def test_valid_pinned_adapter_passes(tmp_path: Path) -> None:
    target = write_target(tmp_path, version="2.0.0-min.1")
    findings = audit_target_adapters(target, REPO, browser_chat=Source("BROWSER_CHAT.md", browser_text(target, version="2.0.0-min.1")))
    assert findings == []


def test_metadata_and_vague_version_drift_detected(tmp_path: Path) -> None:
    target = write_target(tmp_path, version="latest", repo="wrong/repo")
    text = (target / "AGENTS.md").read_text(encoding="utf-8")
    (target / "AGENTS.md").write_text(text.replace("PM_FACING_LANGUAGE = es\n", ""), encoding="utf-8")

    found = codes(audit_target_adapters(target, REPO))

    assert "TAA-META-MISSING" in found
    assert "TAA-META-REPOSITORY" in found
    assert "TAA-VERSION-VAGUE" in found


def test_relative_repository_local_path_is_detected(tmp_path: Path) -> None:
    target = write_target(tmp_path, repository_local_path="relative/target")

    assert "TAA-META-LOCAL-PATH" in codes(audit_target_adapters(target, REPO))


def test_relative_kernel_local_path_is_detected(tmp_path: Path) -> None:
    target = write_target(tmp_path, kernel_local_path="../project-os-v2/kernel")

    assert "TAA-META-KERNEL-PATH" in codes(audit_target_adapters(target, REPO))


def test_roadmap_anchor_errors_detected(tmp_path: Path) -> None:
    target = write_target(tmp_path, roadmap="#274 and #275")
    browser = Source("BROWSER_CHAT.md", browser_text(target, roadmap="https://github.com/other/repo/issues/274"))

    found = codes(audit_target_adapters(target, REPO, browser_chat=browser))

    assert "TAA-ROADMAP-DUPLICATE" in found
    assert "TAA-ROADMAP-REPOSITORY" in found
    assert "TAA-ROADMAP-MISMATCH" in found


def test_missing_roadmap_anchor_detected(tmp_path: Path) -> None:
    target = write_target(tmp_path)
    text = (target / "AGENTS.md").read_text(encoding="utf-8")
    (target / "AGENTS.md").write_text(text.replace("the canonical roadmap issue #274", "the roadmap"), encoding="utf-8")

    assert "TAA-ROADMAP-MISSING" in codes(audit_target_adapters(target, REPO))


def test_live_state_detected_without_flagging_canonical_roadmap(tmp_path: Path) -> None:
    live_state = textwrap.dedent(
        """\
        Current branch: work/123-feature
        Current PR is open.
        Validation passed on pytest.
        Release readiness: ready to release.
        See https://github.com/acme/widgets/issues/99.
        See https://github.com/acme/widgets/pull/12.
        See https://github.com/acme/widgets/commit/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.
        """
    )
    target = write_target(tmp_path, extra=live_state)

    found = codes(audit_target_adapters(target, REPO))

    assert "TAA-LIVE-BRANCH" in found
    assert "TAA-LIVE-PR" in found
    assert "TAA-LIVE-VALIDATION" in found
    assert "TAA-LIVE-RELEASE" in found
    assert "TAA-LIVE-ISSUE-URL" in found
    assert "TAA-LIVE-PR-URL" in found
    assert "TAA-LIVE-COMMIT-URL" in found
    assert "TAA-LIVE-SHA" in found


def test_overlay_removal_between_base_and_worktree_is_detected(tmp_path: Path) -> None:
    protected_notes = "Keep customer data out of fixtures."
    custom_section = textwrap.dedent(
        """\

        ## Security overlay

        Never expose tenant tokens.
        """
    )
    target = write_target(tmp_path, notes=protected_notes, extra=custom_section)
    run_git(target, "init")
    run_git(target, "config", "user.email", "test@example.com")
    run_git(target, "config", "user.name", "Test User")
    run_git(target, "add", "AGENTS.md", "CLAUDE.md")
    run_git(target, "commit", "-m", "base adapter")

    (target / "AGENTS.md").write_text(adapter_text(target, notes="Run local tests."), encoding="utf-8")

    found = codes(audit_target_adapters(target, REPO, base_ref="HEAD"))

    assert "TAA-OVERLAY-CONTENT-REMOVED" in found
    assert "TAA-OVERLAY-SECTION-REMOVED" in found


def test_preserved_or_extended_overlay_is_not_reported(tmp_path: Path) -> None:
    custom_section = textwrap.dedent(
        """\

        ## Security overlay

        Never expose tenant tokens.
        """
    )
    target = write_target(tmp_path, notes="Keep customer data out of fixtures.", extra=custom_section)
    run_git(target, "init")
    run_git(target, "config", "user.email", "test@example.com")
    run_git(target, "config", "user.name", "Test User")
    run_git(target, "add", "AGENTS.md", "CLAUDE.md")
    run_git(target, "commit", "-m", "base adapter")

    extended = custom_section + "\nReview new integrations before enabling them.\n"
    (target / "AGENTS.md").write_text(
        adapter_text(
            target,
            notes="Keep customer data out of fixtures.\nAlso keep generated samples anonymous.",
            extra=extended,
        ),
        encoding="utf-8",
    )

    found = codes(audit_target_adapters(target, REPO, base_ref="HEAD"))

    assert "TAA-OVERLAY-CONTENT-REMOVED" not in found
    assert "TAA-OVERLAY-SECTION-REMOVED" not in found


def test_human_and_json_outputs_report_same_findings(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    target = write_target(tmp_path, version="current")
    human_code = main(["--target", str(target), "--repository", REPO])
    human = capsys.readouterr().out

    json_code = main(["--target", str(target), "--repository", REPO, "--json"])
    payload = json.loads(capsys.readouterr().out)

    human_codes = {line.split(" ", 1)[0] for line in human.splitlines() if line.startswith("TAA-")}
    json_codes = {finding["code"] for finding in payload["findings"]}

    assert human_code == 1
    assert json_code == 1
    assert human_codes == json_codes == {"TAA-VERSION-VAGUE"}


def test_cli_accepts_browser_chat_from_stdin(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = write_target(tmp_path)
    monkeypatch.setattr("sys.stdin", io.StringIO(browser_text(target)))

    assert main(["--target", str(target), "--repository", REPO, "--browser-chat", "-"]) == 0


def test_unreadable_target_is_tooling_error(tmp_path: Path) -> None:
    assert main(["--target", str(tmp_path / "missing"), "--repository", REPO]) == 2
