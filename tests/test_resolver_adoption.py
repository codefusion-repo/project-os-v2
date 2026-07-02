"""Repo-shape guards for issue #315 — adoption of the resolver fast path.

These tests assert the durable adoption behavior in the kernel manifest,
adapters, templates, and docs:

- `kernel/manifest.json` owns surface-aware resolution routing via
  `resolution_strategy`; adapters/templates/docs point to it and never define a
  competing order;
- terminal adapters keep the `tools.project_os_resolve` fast path as the
  manifest's terminal default;
- browser-chat materials resolve manually and never execute repo-local Python;
- manifest/manual resolution stays the canonical fallback;
- resolver output is described as non-authorizing;
- no stale PR/issue/branch/SHA implementation state is stored in durable files.

They guard wording, not kernel rules: the kernel itself is validated by
`tools/validate_kernel.py` and resolved by `tools/project_os_resolve.py`.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

RESOLVER_REF = "tools.project_os_resolve"

MANIFEST = REPO_ROOT / "kernel" / "manifest.json"

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

# Repository-local terminal adapters that should prefer the resolver fast path.
TERMINAL_ADAPTERS = [
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "CLAUDE.md",
    REPO_ROOT / "GEMINI.md",
]

# Target-project terminal adapters must run the resolver from the local Project
# OS checkout, because adopted target repositories may not contain the module.
TARGET_TERMINAL_ADAPTERS = [
    REPO_ROOT / "adapters" / "AGENTS.target.md",
    REPO_ROOT / "adapters" / "CLAUDE.target.md",
    REPO_ROOT / "adapters" / "GEMINI.target.md",
]

ALL_TERMINAL_ADAPTERS = TERMINAL_ADAPTERS + TARGET_TERMINAL_ADAPTERS

BROWSER_CHAT_ADAPTER = REPO_ROOT / "adapters" / "BROWSER_CHAT.target.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestManifestRouting:
    """The manifest owns surface-aware resolution routing (PM decision)."""

    def test_manifest_declares_resolution_strategy(self) -> None:
        strategy = json.loads(_read(MANIFEST)).get("resolution_strategy")
        assert isinstance(strategy, dict), "manifest must declare resolution_strategy"
        blob = " ".join(str(value) for value in strategy.values()).lower()
        # The terminal fast path, browser no-Python rule, canonical fallback, and
        # non-authorizing behavior all live in the manifest, not in adapters.
        assert RESOLVER_REF in blob
        assert "repo-local python" in blob
        assert "canonical fallback" in blob
        assert "boundary.output_not_permission" in blob

    def test_resolution_sequence_points_to_strategy(self) -> None:
        sequence = json.loads(_read(MANIFEST)).get("resolution_sequence", [])
        assert "resolution_strategy" in " ".join(sequence).lower()

    def test_terminal_agents_defer_routing_to_manifest(self) -> None:
        """AGENTS adapters point to the manifest instead of owning a rival order."""
        for path in (REPO_ROOT / "AGENTS.md", REPO_ROOT / "adapters" / "AGENTS.target.md"):
            text = _read(path)
            assert "resolution_strategy" in text, f"{path.name} should point to the manifest strategy"
            assert "competing resolution order" in text, (
                f"{path.name} should state it defines no competing resolution order"
            )


class TestTerminalFastPath:
    """Terminal adapters keep the resolver fast path as the manifest's default."""

    def test_terminal_adapters_mention_resolver(self) -> None:
        for path in ALL_TERMINAL_ADAPTERS:
            assert RESOLVER_REF in _read(path), f"{path.name} should reference {RESOLVER_REF}"

    def test_full_resolver_command_in_canonical_adapters(self) -> None:
        """The full CLI command lives in the canonical AGENTS adapters."""
        for path in (REPO_ROOT / "AGENTS.md", REPO_ROOT / "adapters" / "AGENTS.target.md"):
            text = _read(path)
            assert ".venv/bin/activate" in text
            assert "python -m tools.project_os_resolve" in text
            assert "--kernel-dir \"$KERNEL_LOCAL_PATH\"" in text

    def test_target_adapters_run_resolver_from_project_os_checkout(self) -> None:
        for path in TARGET_TERMINAL_ADAPTERS:
            text = _read(path)
            collapsed = re.sub(r"\s+", " ", text)
            assert "local Project OS checkout" in collapsed, (
                f"{path.name} should name the resolver execution root"
            )
            assert "derived from `KERNEL_LOCAL_PATH`" in collapsed or (
                "PROJECT_OS_LOCAL_PATH" in text
                and "${KERNEL_LOCAL_PATH%/}" in text
                and "${PROJECT_OS_LOCAL_PATH%/kernel}" in text
            ), f"{path.name} should derive the resolver root from KERNEL_LOCAL_PATH"
            assert "target work remains" in collapsed or "live target work anchored" in collapsed, (
                f"{path.name} should keep target work anchored to REPOSITORY_LOCAL_PATH"
            )

    def test_target_agents_resolver_not_invoked_from_target_repo_root(self) -> None:
        text = _read(REPO_ROOT / "adapters" / "AGENTS.target.md")
        resolver_line = "python -m tools.project_os_resolve"
        assert "cd \"$PROJECT_OS_LOCAL_PATH\"\nif [ -d .venv ]; then . .venv/bin/activate; fi\n" + resolver_line in text
        assert "cd \"$REPOSITORY_LOCAL_PATH\"\nif [ -d .venv ]; then . .venv/bin/activate; fi\n" + resolver_line not in text

    def test_no_documented_py_module_invocation(self) -> None:
        """Docs must never tell agents to pass the .py filename to python -m."""
        bad_invocation = f"python -m {RESOLVER_REF}.py"
        bad_invocation_py3 = f"python3 -m {RESOLVER_REF}.py"
        for path in DURABLE_FILES:
            text = _read(path)
            assert bad_invocation not in text
            assert bad_invocation_py3 not in text

    def test_terminal_guidance_names_repo_root_and_kernel_dir(self) -> None:
        """Terminal fast-path prose must keep cwd and kernel path unambiguous."""
        for path in ALL_TERMINAL_ADAPTERS:
            text = _read(path)
            assert "REPOSITORY_LOCAL_PATH" in text, (
                f"{path.name} should explain the live target or repo path"
            )
            assert "--kernel-dir" in text and "KERNEL_LOCAL_PATH" in text, (
                f"{path.name} should pass the configured kernel path explicitly"
            )

    def test_terminal_adapters_keep_manifest_fallback(self) -> None:
        for path in ALL_TERMINAL_ADAPTERS:
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
        text = _read(BROWSER_CHAT_ADAPTER).lower()
        assert "python -m tools.project_os_resolve" not in text
        assert "python3 -m tools.project_os_resolve" not in text

    def test_browser_chat_materials_do_not_require_python_execution(self) -> None:
        text = re.sub(r"\s+", " ", _read(BROWSER_CHAT_ADAPTER).lower())
        forbidden_phrases = (
            "must execute repo-local python",
            "should execute repo-local python",
            "must run repo-local python",
            "should run repo-local python",
            "must use python to resolve",
            "should use python to resolve",
            "run python to resolve the kernel",
        )
        for phrase in forbidden_phrases:
            assert phrase not in text, f"browser chat must not require: {phrase}"


class TestRoutePrompt:
    """Route prompts route to manifest resolution and never own resolver strategy."""

    def test_route_prompt_points_to_manifest(self) -> None:
        assert "kernel/manifest.json" in _read(REPO_ROOT / "templates" / "route-prompt.md")

    def test_route_prompt_does_not_own_resolver_strategy(self) -> None:
        # Resolution is the manifest's; the route prompt must not carry the CLI.
        assert "python3 -m tools.project_os_resolve" not in _read(
            REPO_ROOT / "templates" / "route-prompt.md"
        )


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


class TestSingleEntrypoint:
    """#320: the manifest is the single resolution entrypoint and nothing copies it."""

    def test_manifest_names_itself_single_entrypoint(self) -> None:
        manifest = json.loads(_read(MANIFEST))
        blob = (
            manifest.get("description", "")
            + " "
            + json.dumps(manifest.get("resolution_strategy", {}))
        ).lower()
        assert "single resolution entrypoint" in blob

    def test_durable_files_do_not_copy_resolution_sequence(self) -> None:
        # The numbered resolution_sequence is data owned by the manifest; adapters,
        # templates, and docs point to it and never restate the ordered steps.
        distinctive = "emit exactly one status from statuses.json"
        for path in DURABLE_FILES:
            assert distinctive not in _read(path).lower(), (
                f"{path.name} restates the manifest resolution_sequence"
            )


class TestMeasurementPath:
    """#320: a read-only measurement path reports manual vs fast-path size."""

    def test_measurement_tool_exists_and_is_read_only(self) -> None:
        tool = REPO_ROOT / "tools" / "measure_resolution.py"
        assert tool.exists(), "the resolution size diagnostic must exist"
        text = tool.read_text(encoding="utf-8")
        assert "boundary.output_not_permission" in text
        # It is a diagnostic: it must not perform writes or git/GitHub mutation.
        for forbidden in ("subprocess", "open(", ".write_text", "os.system"):
            assert forbidden not in text, f"measurement tool must not {forbidden}"
