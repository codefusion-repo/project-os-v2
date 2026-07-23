"""Behavioral guards for the internal handoff procedure doc.

These replace the removed prose tests with checks over executable content:
command safety, verification coverage, ordering, stored-state limits, and
reference integrity. Wording stays free to change.
"""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
HANDOFF_PATH = REPO_ROOT / "dogfooding/docs/release/INTERNAL_HANDOFF_READINESS.md"
ADR_PATH = REPO_ROOT / "docs/decisions/0005-public-repository-strategy.md"

# The only commit/tag-object SHAs the docs may store: the immutable v1/v2
# history. Anything else would freeze live state in a durable file.
HISTORICAL_SHAS = {
    "901676d358d37423d8a64896f278075469deb2e8",
    "8b01e9f45b1c2449c9cc799d51ee300b6793e9dc",
    "e9bafbf1b088e9973bd0dc6e5781415ccc09e000",
    "57c6b5176cc43606191418faf884915888cd9202",
}

MUTATING_COMMAND_PATTERNS = (
    r"git\s+fetch",
    r"git\s+tag\s+-[afd]",
    r"git\s+push\s+origin\s+refs/tags/",
    r"git\s+push\s+--delete",
    r"--force",
    r"gh\s+release\s+(?:create|edit|delete|upload|delete-asset)",
)

REQUIRED_READ_ONLY_VERIFICATIONS = (
    "git ls-remote --exit-code --tags origin",
    "git ls-remote --exit-code --heads origin refs/heads/main",
    "gh release view",
    "gh repo view",
    "git tag --list",
    "git status --short --branch",
    "git rev-parse HEAD",
)

MARKDOWN_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def handoff_text() -> str:
    return HANDOFF_PATH.read_text(encoding="utf-8")


def test_handoff_contains_no_tag_or_release_mutation_commands() -> None:
    text = handoff_text()
    for pattern in MUTATING_COMMAND_PATTERNS:
        assert not re.search(pattern, text), f"mutating command present: {pattern}"


def test_handoff_keeps_executable_read_only_verification_coverage() -> None:
    text = handoff_text()
    for command in REQUIRED_READ_ONLY_VERIFICATIONS:
        assert command in text, f"read-only verification missing: {command}"


def test_handoff_preflight_checks_tag_absence_then_worktree_then_head() -> None:
    text = handoff_text()
    positions = [
        text.index("git tag --list"),
        text.index("git status --short --branch"),
        text.index("git rev-parse HEAD"),
    ]
    assert positions == sorted(positions)


def test_handoff_and_adr_store_no_live_shas_beyond_the_historical_baseline() -> None:
    for path in (HANDOFF_PATH, ADR_PATH):
        found = set(re.findall(r"\b[0-9a-f]{40}\b", path.read_text(encoding="utf-8")))
        assert found <= HISTORICAL_SHAS, f"{path.name} stores non-historical SHAs: {found - HISTORICAL_SHAS}"


def test_handoff_requires_separate_exact_pm_approvals() -> None:
    # The tag and the internal release each need their own exact PM approval;
    # a single merged approval would weaken boundary.separate_pm_approval.
    text = handoff_text()
    approvals = re.findall(r"aprobaci[oó]n PM exacta", text, re.IGNORECASE)
    assert len(approvals) >= 2


def test_dogfooding_docs_relative_links_resolve() -> None:
    missing: list[str] = []
    for source in sorted((REPO_ROOT / "dogfooding/docs").rglob("*.md")):
        text = source.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK_PATTERN.findall(text):
            target = raw_target.strip().split()[0].strip("<>").split("#", 1)[0]
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            if not (source.parent / target).resolve().exists():
                missing.append(f"{source.relative_to(REPO_ROOT)} -> {raw_target}")
    assert missing == []


def test_handoff_adr_anchor_references_match_real_adr_headings() -> None:
    adr_text = ADR_PATH.read_text(encoding="utf-8")
    anchors = {
        target.split("#", 1)[1]
        for target in MARKDOWN_LINK_PATTERN.findall(handoff_text())
        if "#" in target and "decisions/0005" in target
    }
    assert anchors
    headings = {
        re.sub(r"[^a-z0-9\s-]", "", heading.lower()).strip().replace(" ", "-")
        for heading in re.findall(r"^#{1,6}\s+(.+)$", adr_text, re.MULTILINE)
    }
    for anchor in anchors:
        assert anchor in headings, f"handoff references missing ADR anchor: #{anchor}"
