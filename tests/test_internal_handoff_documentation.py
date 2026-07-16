"""Stable guards for the reconciled internal handoff documentation."""

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ADR_PATH = REPO_ROOT / "docs/decisions/0005-public-repository-strategy.md"
HANDOFF_PATH = REPO_ROOT / "docs/release/INTERNAL_HANDOFF_READINESS.md"
TAG_NAME = "project-os-internal-handoff-v1"
BASELINE_SHA = "8b01e9f45b1c2449c9cc799d51ee300b6793e9dc"
TAG_OBJECT_SHA = "901676d358d37423d8a64896f278075469deb2e8"
CURRENT_DECISION_URL = (
    "https://github.com/codefusion-repo/project-os-v2/issues/424"
    "#issuecomment-4987453334"
)


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
    assert CURRENT_DECISION_URL in text
    assert "2026-07-15T03:30:23Z" in text
    assert "2026-07-16T02:14:10Z" in text
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
    assert "no se congelan en este archivo: se releen en GitHub" in text
    assert set(re.findall(r"\b[0-9a-f]{40}\b", text)) == {
        BASELINE_SHA,
        TAG_OBJECT_SHA,
    }


def test_handoff_verification_works_without_local_tags_or_fresh_tracking_refs() -> None:
    text = HANDOFF_PATH.read_text(encoding="utf-8")

    assert "git ls-remote --exit-code --tags origin" in text
    assert "'refs/tags/project-os-internal-handoff-v1^{}'" in text
    assert TAG_OBJECT_SHA in text
    assert "git ls-remote --exit-code --heads origin refs/heads/main" in text
    assert "No requiere tag local" in text
    assert "no dependen de remote-tracking" in text
    assert "git cat-file" not in text
    assert "git rev-parse origin/main" not in text


def test_handoff_contains_no_tag_or_release_mutation_commands() -> None:
    text = HANDOFF_PATH.read_text(encoding="utf-8")

    for forbidden_mutation in (
        "git fetch",
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
        "git ls-remote --exit-code --tags origin",
        "git ls-remote --exit-code --heads origin refs/heads/main",
        "gh release view project-os-internal-handoff-v1",
        "gh repo view codefusion-repo/project-os-v2",
    ):
        assert required_verification in text


def test_handoff_distinguishes_approved_title_from_live_release_metadata() -> None:
    text = HANDOFF_PATH.read_text(encoding="utf-8")

    assert CURRENT_DECISION_URL in text
    assert "Título aprobado/histórico del GitHub Release" in text
    assert "El `name` vivo del Release" in text
    assert "reporta drift y falla" in text


def test_later_release_decision_does_not_expand_other_authority() -> None:
    text = HANDOFF_PATH.read_text(encoding="utf-8")

    for preserved_limit in (
        "visibilidad, settings, cierre",
        "archivo del repositorio",
        "creación de `agent-os-cli`",
        "transición de contenido",
        "sincronización o backports",
        "Cierre de issue #424",
        "Cierre de roadmap #274",
    ):
        assert preserved_limit in text


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
