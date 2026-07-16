"""Stable guards for the reconciled internal handoff documentation."""

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ADR_PATH = REPO_ROOT / "docs/decisions/0005-public-repository-strategy.md"
HANDOFF_PATH = REPO_ROOT / "docs/release/INTERNAL_HANDOFF_READINESS.md"
TAG_NAME = "project-os-internal-handoff-v1"
BASELINE_SHA = "8b01e9f45b1c2449c9cc799d51ee300b6793e9dc"


def test_adr_preserves_history_and_bounds_the_later_release_decision() -> None:
    text = ADR_PATH.read_text(encoding="utf-8")

    assert "## Amendment 1 — bounded internal handoff tag exception (issue #424)" in text
    assert (
        "## Amendment 2 — exact internal GitHub Release for the fixed handoff "
        "baseline (issue #424)"
    ) in text
    assert "supersedes the earlier tag-only exclusion and no other action" in text
    assert "They are not retroactively rewritten" in text
    assert TAG_NAME in text
    assert BASELINE_SHA in text
    for preserved_boundary in (
        "does not authorize a visibility or settings change",
        "does not close issue #424 or roadmap #274",
        "the sole source of truth for future Project OS development",
    ):
        assert preserved_boundary in text


def test_handoff_fixes_the_baseline_without_storing_the_current_main_head() -> None:
    text = HANDOFF_PATH.read_text(encoding="utf-8")

    assert TAG_NAME in text
    assert BASELINE_SHA in text
    assert "Project OS internal handoff baseline" in text
    assert "head permanentemente actual de `main`" in text
    assert "su estado operativo se verifica en GitHub" in text
    assert set(re.findall(r"\b[0-9a-f]{40}\b", text)) == {BASELINE_SHA}


def test_handoff_contains_only_read_only_tag_and_release_commands() -> None:
    text = HANDOFF_PATH.read_text(encoding="utf-8")

    for forbidden_mutation in (
        "git tag -a",
        "git push origin refs/tags/",
        "gh release create",
        "gh release edit",
        "gh release delete",
        "git tag -d",
        "git push --delete",
    ):
        assert forbidden_mutation not in text
    for required_verification in (
        "git ls-remote --tags origin",
        "git cat-file -t",
        "git rev-parse 'project-os-internal-handoff-v1^{}'",
        "gh release view project-os-internal-handoff-v1",
        "gh repo view codefusion-repo/project-os-v2",
    ):
        assert required_verification in text


def test_handoff_relative_targets_and_adr_anchors_exist() -> None:
    adr = ADR_PATH.read_text(encoding="utf-8")

    relative_targets = (
        "../decisions/0005-public-repository-strategy.md",
        "../security/PUBLIC_READINESS_REVIEW.md",
        "../decisions/0004-public-presentation-and-packaging.md",
    )
    for relative_target in relative_targets:
        assert (HANDOFF_PATH.parent / relative_target).resolve().is_file()
    assert "## Amendment 1 — bounded internal handoff tag exception (issue #424)" in adr
    assert (
        "## Amendment 2 — exact internal GitHub Release for the fixed handoff "
        "baseline (issue #424)"
    ) in adr
