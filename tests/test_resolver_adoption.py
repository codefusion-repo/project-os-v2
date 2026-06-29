"""Repo-shape guards for issue #315 — adoption of the resolver fast path.

These tests assert the durable adoption behavior in adapters, templates, and
docs:

- terminal adapters/templates point at the `tools.project_os_resolve` fast path;
- browser-chat materials resolve manually and never execute repo-local Python;
- manifest/manual resolution stays the canonical fallback;
- resolver output is described as non-authorizing;
- no stale PR/issue/branch/SHA implementation state is stored in durable files.

They guard wording, not kernel rules: the kernel itself is validated by
`tools/validate_kernel.py` and resolved by `tools/project_os_resolve.py`.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

RESOLVER_REF = "tools.project_os_resolve"

# Durable Project OS materials that mention kernel resolution and must stay
# free of live implementation state.
DURABLE_FILES = [
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "CLAUDE.md",
    REPO_ROOT / "GEMINI.md",
    REPO_ROOT / "adapters" / "AGENTS.target.md",
    REPO_ROOT / "adapters" / "CLAUDE.target.md",
    REPO_ROOT / "adapters" / "GEMINI.target.md",
    REPO_ROOT / "adapters" / "BROWSER_CHAT.target.md",
    REPO_ROOT / "templates" / "route-prompt.md",
    REPO_ROOT / "docs" / "DESIGN.md",
    REPO_ROOT / "README.md",
    REPO_ROOT / "docs" / "GETTING_STARTED.md",
    REPO_ROOT / "docs" / "PUBLIC_USAGE_MODEL.md",
]

# Public-facing docs that explain kernel resolution to readers. They must
# distinguish the terminal fast path from manual/manifest resolution and keep
# resolver output non-authorizing, without restating kernel rules.
PUBLIC_DOCS = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "docs" / "GETTING_STARTED.md",
    REPO_ROOT / "docs" / "PUBLIC_USAGE_MODEL.md",
]

# Docs whose resolution prose also covers browser/non-terminal surfaces and so
# must state that those surfaces do not run repo-local Python.
PUBLIC_DOCS_WITH_BROWSER = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "docs" / "PUBLIC_USAGE_MODEL.md",
]

# Either-language phrasings that tie resolver output to "grants no permission".
NON_AUTHORIZING_PHRASES = ("grants no permission", "no otorga permiso")

# Terminal-capable adapters that should prefer the resolver fast path.
TERMINAL_ADAPTERS = [
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "CLAUDE.md",
    REPO_ROOT / "GEMINI.md",
    REPO_ROOT / "adapters" / "AGENTS.target.md",
    REPO_ROOT / "adapters" / "CLAUDE.target.md",
    REPO_ROOT / "adapters" / "GEMINI.target.md",
]

BROWSER_CHAT_ADAPTER = REPO_ROOT / "adapters" / "BROWSER_CHAT.target.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestTerminalFastPath:
    """Terminal adapters prefer the resolver fast path with manual fallback."""

    def test_terminal_adapters_mention_resolver(self) -> None:
        for path in TERMINAL_ADAPTERS:
            assert RESOLVER_REF in _read(path), f"{path.name} should reference {RESOLVER_REF}"

    def test_full_resolver_command_in_canonical_adapters(self) -> None:
        """The full CLI command lives in the canonical AGENTS adapters."""
        for path in (REPO_ROOT / "AGENTS.md", REPO_ROOT / "adapters" / "AGENTS.target.md"):
            assert "python3 -m tools.project_os_resolve" in _read(path)

    def test_terminal_adapters_keep_manifest_fallback(self) -> None:
        for path in TERMINAL_ADAPTERS:
            text = _read(path)
            assert "manifest" in text.lower(), f"{path.name} should keep manifest resolution"


class TestBrowserChatNoPython:
    """Browser chat resolves manually and never executes repo-local Python."""

    def test_browser_chat_states_no_python(self) -> None:
        # Collapse whitespace so line wraps in the prose do not hide the phrase.
        text = re.sub(r"\s+", " ", _read(BROWSER_CHAT_ADAPTER).lower())
        assert "does not execute repo-local python" in text
        # The first-message activation block must also forbid repo-local Python.
        assert text.count("repo-local python") >= 2

    def test_browser_chat_resolves_via_manifest(self) -> None:
        assert "manifest.json" in _read(BROWSER_CHAT_ADAPTER)

    def test_browser_chat_does_not_instruct_running_resolver(self) -> None:
        """The resolver CLI command must not be given as a browser-chat step."""
        assert "python3 -m tools.project_os_resolve" not in _read(BROWSER_CHAT_ADAPTER)


class TestRoutePrompt:
    """Route-prompt guidance mentions the fast path, copy-safe."""

    def test_route_prompt_mentions_fast_path(self) -> None:
        assert RESOLVER_REF in _read(REPO_ROOT / "templates" / "route-prompt.md")


class TestDesignDoc:
    """DESIGN.md frames the resolver as a non-authorizing accelerator."""

    def test_design_describes_resolver(self) -> None:
        text = _read(REPO_ROOT / "docs" / "DESIGN.md")
        assert "project_os_resolve" in text
        assert "second source of truth" in text
        assert "boundary.output_not_permission" in text


class TestPublicDocs:
    """Public docs distinguish the terminal fast path from manual resolution."""

    def test_public_docs_mention_resolver_fast_path(self) -> None:
        for path in PUBLIC_DOCS:
            assert RESOLVER_REF in _read(path), (
                f"{path.name} should reference the {RESOLVER_REF} fast path"
            )

    def test_public_docs_keep_manifest_manual_fallback(self) -> None:
        for path in PUBLIC_DOCS:
            text = _read(path).lower()
            assert "manifest" in text, f"{path.name} should keep manifest resolution"
            assert "fallback" in text, (
                f"{path.name} should keep manual resolution as the canonical fallback"
            )

    def test_public_docs_describe_resolver_as_non_authorizing(self) -> None:
        for path in PUBLIC_DOCS:
            text = re.sub(r"\s+", " ", _read(path).lower())
            assert any(phrase in text for phrase in NON_AUTHORIZING_PHRASES), (
                f"{path.name} should describe resolver output as non-authorizing"
            )

    def test_public_docs_state_browser_no_repo_local_python(self) -> None:
        for path in PUBLIC_DOCS_WITH_BROWSER:
            text = re.sub(r"\s+", " ", _read(path).lower())
            assert "repo-local python" in text, (
                f"{path.name} should state browser/non-terminal surfaces "
                f"do not run repo-local Python"
            )


class TestNonAuthorizing:
    """Resolver output is explicitly described as non-authorizing."""

    def test_resolver_output_not_permission(self) -> None:
        # Canonical adapters and the design doc must tie the resolver to the
        # output-not-permission boundary.
        for path in (
            REPO_ROOT / "AGENTS.md",
            REPO_ROOT / "adapters" / "AGENTS.target.md",
            REPO_ROOT / "docs" / "DESIGN.md",
        ):
            assert "boundary.output_not_permission" in _read(path)


class TestNoStaleLiveState:
    """No stale PR/issue/branch/SHA implementation state in durable files."""

    # Stale-state patterns issue #315 forbids introducing into durable files.
    STALE_PATTERNS = [
        re.compile(r"PR\s*#\d"),
        re.compile(r"#31[0-9]\b"),  # issues/PRs in this adoption's neighborhood
        re.compile(r"#307\b"),
        re.compile(r"work/\d"),  # concrete work branch names
        re.compile(r"\b(?=[0-9a-f]*\d)[0-9a-f]{7,40}\b"),  # commit SHAs
    ]

    def test_no_stale_state_in_durable_files(self) -> None:
        for path in DURABLE_FILES:
            text = _read(path)
            for pattern in self.STALE_PATTERNS:
                match = pattern.search(text)
                assert match is None, (
                    f"{path.name} contains stale live-state token "
                    f"{match.group(0)!r} (pattern {pattern.pattern})"
                )
