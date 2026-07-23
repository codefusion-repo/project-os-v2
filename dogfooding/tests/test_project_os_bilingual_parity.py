"""Stable-contract guards for the parallel Spanish and English surfaces."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from tools.operation_prompt_wizard import discover_operations
from dogfooding.tools.project_os_parity import build_report, load_kernel
from tools.project_os_resolve import DEFAULT_KERNEL_DIR, resolve
from tools.project_os_surfaces import SURFACES
from tools.validate_kernel import validate_kernel


REPO_ROOT = Path(__file__).resolve().parents[2]
ES_KERNEL = REPO_ROOT / "project-os-es/kernel"
EN_KERNEL = REPO_ROOT / "project-os-en/kernel"
SECRET_PATTERN = re.compile(
    r"\b(?:gh[pousr]_[A-Za-z0-9_]{12,}|github_pat_[A-Za-z0-9_]{20,}|"
    r"sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{12,})\b"
)
LIVE_GITHUB_OBJECT_PATTERN = re.compile(
    r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/(?:issues|pull|commit|tree)/[A-Za-z0-9_.-]+"
)
SPANISH_PROSE_PATTERN = re.compile(
    r"\b(?:la|las|los|una|para|porque|antes|después|requeridas|opcionales|entrega|"
    r"conexiones|cuida|hace|draftea|ejecuta|revisa|procesa|audita|analiza|operación|"
    r"aprobación|evidencia|validación|despliegue|seguridad|estado|ruta|archivo|rama|"
    r"cerrado|faltante|ambigua|fase|aplica|inglés|español)\b",
    re.IGNORECASE,
)
# These machine values and variable names are stable contracts, not prose.
SPANISH_TOKEN_ALLOWLIST = ("no_resuelto", "resuelto", "PM_FEEDBACK_HUMANO", "PM_QUESTION_HUMANO")


def test_kernel_and_operation_contracts_have_no_parity_findings() -> None:
    report = build_report()

    assert report["surfaces"] == {
        "default": "project-os-es",
        "explicit_english": "project-os-en",
    }
    assert report["findings"] == []
    assert report["kernel_ids"]
    assert report["reference_edges"] > 0
    assert report["operations"]["mos_codes"] == 121
    assert report["operations"]["path_matrix"]
    assert report["structural_findings"] == []
    assert report["semantic_invariant_findings"] == []
    assert report["manual_review_required"] == [
        "natural PM-facing English across all operation and template pairs",
        "full semantic fidelity beyond automated critical invariants",
    ]


def test_mos_r3_keeps_exact_bilingual_variable_contract() -> None:
    """The wizard parses these variables; the contract must match across surfaces."""
    expected = (
        ("DECISION_SOURCE", True),
        ("PM_DECISION_ALREADY_MADE", True),
        ("ISSUE_NUMBER", False),
        ("PR_NUMBER", False),
        ("DECISION_OPTIONS", False),
        ("PM_DECISION", False),
    )
    for operations_dir in (
        REPO_ROOT / "project-os-es" / "operaciones",
        REPO_ROOT / "project-os-en" / "operations",
    ):
        operation = next(
            item for item in discover_operations(operations_dir) if item.mos_code == "MOS-R.3"
        )
        assert tuple((variable.name, variable.required) for variable in operation.variables) == expected


def test_mos_0_1_keeps_exact_bilingual_variable_contract() -> None:
    """The wizard parses these variables; the contract must match across surfaces."""
    expected = (
        ("TARGET_REPOSITORY", True),
        ("PM_FEEDBACK_HUMANO", False),
        ("PM_QUESTION_HUMANO", False),
    )
    for operations_dir in (
        REPO_ROOT / "project-os-es" / "operaciones",
        REPO_ROOT / "project-os-en" / "operations",
    ):
        operation = next(
            item for item in discover_operations(operations_dir) if item.mos_code == "MOS-0.1"
        )
        assert tuple((variable.name, variable.required) for variable in operation.variables) == expected


def test_route_prompt_template_declares_wizard_consumed_fields_and_bundle_stays_copy_safe() -> None:
    """The wizard fills these route-prompt fields; the bundle commands are PM-executed shell."""
    templates = REPO_ROOT / "project-os-en/templates"
    route = (templates / "route-prompt.md").read_text(encoding="utf-8")
    bundle = (templates / "pm-command-bundle.md").read_text(encoding="utf-8")

    for field in (
        "OPTIONAL_SKILL",
        "HYDRATION_LEVEL",
        "RECOMMENDED_TERMINAL_AGENT_FAMILY",
        "PM_AUTHORIZATION_STATUS",
        "recommended_effort",
    ):
        assert field in route

    for command_pattern in (
        "--body-file",
        "set -e",
        "set -u",
        "set -o pipefail",
        "gh pr ready",
        "--merge --delete-branch",
        "--match-head-commit",
        "gh issue close",
        "git -C <local-path> branch -D <work-branch>",
    ):
        assert command_pattern in bundle
    assert "--squash" not in bundle


def test_pm_command_bundle_uses_rest_for_body_only_issue_and_pr_edits() -> None:
    for surface in ("project-os-es", "project-os-en"):
        bundle = (REPO_ROOT / surface / "templates/pm-command-bundle.md").read_text(
            encoding="utf-8"
        )
        issue_block = re.search(
            r"```sh\n(?P<body>cat > /tmp/issue-body\.md.*?\n)```", bundle, re.DOTALL
        )
        pr_block = re.search(
            r"```sh\n(?P<body>cat > /tmp/pr-body\.md.*?\n)```", bundle, re.DOTALL
        )

        assert issue_block and pr_block
        issue_commands = issue_block.group("body")
        pr_commands = pr_block.group("body")

        for commands, endpoint, body_file in (
            (issue_commands, "repos/<owner>/<repo>/issues/<issue-number>", "/tmp/issue-body.md"),
            (pr_commands, "repos/<owner>/<repo>/pulls/<pr-number>", "/tmp/pr-body.md"),
        ):
            assert f'gh api --method PATCH "{endpoint}"' in commands
            assert f'-F "body=@{body_file}" --silent' in commands
            assert f'gh api --method GET "{endpoint}"' in commands
            assert commands.count(endpoint) == 2

        assert "/pulls/" not in issue_commands
        assert "/issues/" not in pr_commands
        assert "gh issue edit" not in issue_commands
        assert "gh pr edit" not in pr_commands


def test_both_kernels_validate_and_default_remains_spanish() -> None:
    assert DEFAULT_KERNEL_DIR == ES_KERNEL
    assert validate_kernel(ES_KERNEL) == []
    assert validate_kernel(EN_KERNEL) == []
    assert resolve("actor.browser_chat", "workflow.pm_intake", "mode.review_only")["resuelto"]["manifest"]["language"] == "es"


@pytest.mark.parametrize(
    ("actor", "workflow", "mode"),
    (
        ("actor.browser_chat", "workflow.pm_intake", "mode.review_only"),
        ("actor.terminal_agent", "workflow.issue_implementation", "mode.delegated_commit_pr"),
        ("actor.browser_chat", "workflow.review_before_close", "mode.review_only"),
    ),
)
def test_required_resolver_smokes_pass_in_both_languages(actor: str, workflow: str, mode: str) -> None:
    spanish = resolve(actor, workflow, mode, kernel_dir=ES_KERNEL)
    english = resolve(actor, workflow, mode, kernel_dir=EN_KERNEL)

    assert spanish["estado"] == english["estado"] == "status.resolved"
    assert spanish["resuelto"]["manifest"]["language"] == "es"
    assert english["resuelto"]["manifest"]["language"] == "en"
    assert set(item["key"] for item in spanish["resuelto"]["workflow"]["required_evidence"]) == set(
        item["key"] for item in english["resuelto"]["workflow"]["required_evidence"]
    )
    assert set(item["key"] for item in spanish["resuelto"]["workflow"]["allowed_outputs"]) == set(
        item["key"] for item in english["resuelto"]["workflow"]["allowed_outputs"]
    )


def test_every_artifact_template_and_active_skill_resolves_in_both_languages() -> None:
    routes = {
        "workflow.review_only": ("actor.browser_chat", "mode.review_only"),
        "workflow.issue_implementation": ("actor.terminal_agent", "mode.delegated_commit_pr"),
        "workflow.issue_implementation_manual": ("actor.browser_chat", "mode.review_only"),
        "workflow.review_before_close": ("actor.browser_chat", "mode.review_only"),
        "workflow.implementation_discipline_audit": ("actor.browser_chat", "mode.review_only"),
        "workflow.pm_intake": ("actor.browser_chat", "mode.review_only"),
        "workflow.design_asset": ("actor.browser_chat", "mode.review_only"),
        "workflow.security_revision": ("actor.browser_chat", "mode.review_only"),
        "workflow.release_readiness": ("actor.browser_chat", "mode.review_only"),
        "workflow.handoff": ("actor.browser_chat", "mode.review_only"),
        "workflow.target_adoption": ("actor.terminal_agent", "mode.delegated_commit_pr"),
        "workflow.deployment": ("actor.terminal_agent", "mode.delegated_deploy_execution"),
    }
    for surface, kernel_dir in zip(SURFACES, (ES_KERNEL, EN_KERNEL), strict=True):
        kernel = load_kernel(surface)
        expected_artifacts = {item["key"] for item in kernel["artifacts"]}
        resolved_artifacts: set[str] = set()
        for workflow, (actor, mode) in routes.items():
            result = resolve(actor, workflow, mode, kernel_dir=kernel_dir)
            assert result["estado"] == "status.resolved"
            for artifact in result["resuelto"]["workflow"]["artefactos"]:
                resolved_artifacts.add(artifact["key"])
                assert (REPO_ROOT / artifact["required_template"]).is_file()
        assert resolved_artifacts == expected_artifacts

        for skill in kernel["skills"]:
            result = resolve(
                "actor.browser_chat",
                "workflow.pm_intake",
                "mode.review_only",
                kernel_dir=kernel_dir,
                skill=skill["key"],
            )
            assert result["estado"] == "status.resolved"
            assert result["resuelto"]["requested_skills"][0]["key"] == skill["key"]
            assert (REPO_ROOT / result["resuelto"]["requested_skills"][0]["required_skill"]).is_file()


def test_unknown_skill_and_unallowed_kernel_paths_fail_closed() -> None:
    unknown = resolve(
        "actor.browser_chat",
        "workflow.pm_intake",
        "mode.review_only",
        kernel_dir=EN_KERNEL,
        skill="skill.unknown",
    )
    assert unknown["estado"] == "status.blocked"
    assert "unknown skill" in unknown["errores"][0]

    for invalid in (REPO_ROOT / "kernel", REPO_ROOT / "project-os-en", REPO_ROOT / "project-os-en/kernel/extra"):
        result = resolve("actor.browser_chat", "workflow.pm_intake", "mode.review_only", kernel_dir=invalid)
        assert result["estado"] == "status.blocked"
        assert result["resuelto"] is None


def test_wizard_discovers_and_parses_explicit_english_catalog() -> None:
    spanish = discover_operations(REPO_ROOT / "project-os-es/operaciones")
    english = discover_operations(REPO_ROOT / "project-os-en/operations")

    assert len(spanish) == len(english) == 121
    assert {item.mos_code for item in spanish} == {item.mos_code for item in english}
    assert all(item.description and item.phase_label for item in english)
    assert any(item.variables for item in english)
    assert {item.phase_path for item in english} == {
        "cross-phase",
        "phase-0",
        "phase-1",
        "phase-2",
        "phase-3",
        "phase-4",
        "phase-5",
        "phase-6",
    }


def test_adapter_responsibilities_and_boundaries_are_preserved() -> None:
    for root_name, language in (("project-os-es", "es"), ("project-os-en", "en")):
        root = REPO_ROOT / root_name / "adapters"
        agents = (root / "AGENTS.target.md").read_text(encoding="utf-8")
        browser = (root / "BROWSER_CHAT.target.md").read_text(encoding="utf-8")
        fields = [
            "PROJECT_NAME =",
            "REPOSITORY_NAME =",
            "REPOSITORY_LOCAL_PATH =",
            "DEFAULT_BRANCH =",
            "WORK_BRANCH_PATTERN =",
            "PM_FACING_LANGUAGE =",
            "KERNEL_REPOSITORY =",
            "KERNEL_LOCAL_PATH =",
            "KERNEL_VERSION_ADOPTED =",
        ]
        positions = [agents.index(field) for field in fields]
        assert positions == sorted(positions)
        assert f"PM_FACING_LANGUAGE = {language}" in agents
        assert "REPOSITORY_LOCAL_PATH = $PROJECT_OS_TARGET_ROOT" in agents
        assert "KERNEL_LOCAL_PATH = $PROJECT_OS_KERNEL_DIR" in agents
        assert "PROJECT_OS_TARGET_ROOT" in agents
        assert "PROJECT_OS_KERNEL_DIR" in agents
        assert "$PWD" not in agents
        assert "tools/project_os_resolve.py" in agents
        assert "AGENTS.md" in agents
        assert "BROWSER_CHAT.md" in browser
        assert "read-only" in browser
        assert "draft-only" in browser
        assert "Python" in browser
        for shim in ("CLAUDE.target.md", "GEMINI.target.md"):
            text = (root / shim).read_text(encoding="utf-8")
            assert "AGENTS.md" in text
            assert "KERNEL_LOCAL_PATH =" not in text


def test_english_surface_has_no_accidental_spanish_prose_or_legacy_paths() -> None:
    hits: list[str] = []
    legacy = "legacy-" + "project-os"
    removed_resolver = "project-os-es/" + "tools/resolver.py"
    for path in sorted((REPO_ROOT / "project-os-en").rglob("*")):
        if not path.is_file() or path.suffix not in {".md", ".json"}:
            continue
        text = path.read_text(encoding="utf-8")
        for allowed in SPANISH_TOKEN_ALLOWLIST:
            text = text.replace(allowed, "")
        if match := SPANISH_PROSE_PATTERN.search(text):
            hits.append(f"{path.relative_to(REPO_ROOT)}: {match.group(0)}")
        assert legacy not in text
        assert removed_resolver not in text
        assert not SECRET_PATTERN.search(text)
        assert not LIVE_GITHUB_OBJECT_PATTERN.search(text)
        assert not re.search(r"\b[0-9a-f]{40}\b", text, re.IGNORECASE)
    assert hits == []


def test_only_one_principal_resolver_exists() -> None:
    assert [path.name for path in (REPO_ROOT / "tools").glob("*resolve*.py")] == [
        "project_os_resolve.py"
    ]
    assert not list((REPO_ROOT / "project-os-es").rglob("*resolver*.py"))
    assert not list((REPO_ROOT / "project-os-en").rglob("*resolver*.py"))
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "español, default" in readme
    assert "selección explícita" in readme
