"""Stable-contract guards for the parallel Spanish and English surfaces."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from tools.operation_prompt_wizard import discover_operations
from tools.project_os_parity import build_report, load_kernel
from tools.project_os_resolve import DEFAULT_KERNEL_DIR, resolve
from tools.project_os_surfaces import SURFACES
from tools.validate_kernel import validate_kernel


REPO_ROOT = Path(__file__).resolve().parents[1]
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
# This is intentionally a narrow regression list, not a grammar checker. These
# third-person forms occurred as the first significant word of Does/How sections.
THIRD_PERSON_OPERATION_VERBS = frozenset(
    {
        "Analyzes",
        "Checks",
        "Classifies",
        "Converts",
        "Derives",
        "Encapsulates",
        "Establishes",
        "Evaluates",
        "Identifies",
        "Iterates",
        "Packages",
        "Processes",
        "Reads",
        "Refers",
        "Refreshes",
        "Resolves",
        "Sorts",
        "Summarizes",
        "Synthesizes",
        "Updates",
        "Uses",
        "Validates",
    }
)


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


def test_english_operations_keep_semantic_sections_safeguards_and_natural_titles() -> None:
    spanish = {
        item.mos_code: item
        for item in discover_operations(REPO_ROOT / "project-os-es/operaciones")
    }
    english = {
        item.mos_code: item
        for item in discover_operations(REPO_ROOT / "project-os-en/operations")
    }
    boilerplate = (
        "Complete this lifecycle outcome through the selected workflow "
        "with explicit evidence and boundaries."
    )

    assert set(spanish) == set(english)
    for code, operation in english.items():
        for label in ("Does", "For", "How", "Deliver"):
            match = re.search(rf"^\*\*{label}:\*\*\s*(.+)$", operation.text, re.MULTILINE)
            assert match and match.group(1).strip(), f"{code} has an empty {label} section"
        assert boilerplate not in operation.text
        assert ("**Cuida**" in spanish[code].text) == ("**Safeguards**" in operation.text)
        assert "PRocess" not in operation.text.splitlines()[0]
        assert not re.search(r"\bReview pr\b", operation.text.splitlines()[0])


def test_mos_r3_keeps_exact_bilingual_variable_contract_and_semantics() -> None:
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

    english = (
        REPO_ROOT / "project-os-en/operations/cross-phase/MOS-R.3-process-needs-pm-decision.md"
    ).read_text(encoding="utf-8").lower()
    for clause in (
        "live evidence",
        "impact",
        "tradeoffs",
        "recommendation",
        "exact question",
        "never authorizes",
        "status.needs_context",
        "status.needs_pm_decision",
        "both may remain blank",
        "derive context",
        "unrelated",
    ):
        assert clause in english

    related_flow_guards = {
        REPO_ROOT / "project-os-es/operaciones/cross-fase/MOS-R.3-procesar-decision-pm-pendiente.md": (
            "flujo relacionado verificable",
            "no están relacionadas, falla cerrado",
            "ambas pueden quedar vacías",
            "deriva el contexto",
        ),
        REPO_ROOT / "project-os-en/operations/cross-phase/MOS-R.3-process-needs-pm-decision.md": (
            "verifiably related flow",
            "they are unrelated, fail closed",
            "both may remain blank",
            "derive context",
        ),
    }
    for path, clauses in related_flow_guards.items():
        text = path.read_text(encoding="utf-8").lower()
        for clause in clauses:
            assert clause in text


def test_mos_0_1_requires_target_repository_and_fails_closed_bilingually() -> None:
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

    fail_closed_clauses = {
        REPO_ROOT / "project-os-es/operaciones/fase-0/MOS-0.1-activar-sesion-browser-chat.md": (
            "`owner/repo`",
            "`status.needs_context`",
            "está ausente",
            "corresponde a otro repositorio",
            "nunca usa silenciosamente otro repositorio conectado",
            "read-only y draft-only",
            "exclusivamente contra `TARGET_REPOSITORY`",
            "identificando explícitamente el target revisado",
        ),
        REPO_ROOT / "project-os-en/operations/phase-0/MOS-0.1-activate-browser-session.md": (
            "`owner/repo`",
            "`status.needs_context`",
            "is absent",
            "belongs to another repository",
            "never silently use another connected repository",
            "read-only and draft-only",
            "exclusively against `TARGET_REPOSITORY`",
            "naming the reviewed target explicitly",
        ),
    }
    for path, clauses in fail_closed_clauses.items():
        text = path.read_text(encoding="utf-8")
        for clause in clauses:
            assert clause in text, f"{path.name} lost fail-closed clause: {clause}"

    guide_clauses = {
        REPO_ROOT / "project-os-es/docs/empezar.md": (
            "declarando `TARGET_REPOSITORY` en formato `owner/repo`",
            "solicita\n   el target antes de resolver el estado inicial",
        ),
        REPO_ROOT / "project-os-en/docs/getting-started.md": (
            "declaring `TARGET_REPOSITORY` in `owner/repo` format",
            "asks for\n   the target before resolving the initial state",
        ),
    }
    for path, clauses in guide_clauses.items():
        text = path.read_text(encoding="utf-8")
        for clause in clauses:
            assert clause in text, f"{path.name} lost activation-target guidance: {clause}"


def test_english_operation_does_and_how_avoid_known_third_person_regressions() -> None:
    """Protect the observed voice regression without attempting general grammar validation."""
    operations = discover_operations(REPO_ROOT / "project-os-en/operations")

    assert len(operations) == 121
    for operation in operations:
        for label in ("Does", "How"):
            match = re.search(rf"^\*\*{label}:\*\*\s*(.+)$", operation.text, re.MULTILINE)
            assert match and match.group(1).strip(), f"{operation.mos_code} has an empty {label} section"
            first_word = re.search(r"[A-Za-z]+(?:-[A-Za-z]+)?", match.group(1))
            assert first_word, f"{operation.mos_code} has no significant word in {label}"
            assert first_word.group(0) not in THIRD_PERSON_OPERATION_VERBS, (
                f"{operation.mos_code} starts {label} with a known third-person verb: "
                f"{first_word.group(0)}"
            )


def test_route_prompt_and_pm_command_bundle_keep_authorization_contracts() -> None:
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
    for clause in ("re-resolves the kernel", "reads live evidence", "fails closed"):
        assert clause in route
    assert "do not grant permission" in route
    assert "replace exact PM approval" in route
    assert "was not delivered by the PM" in route
    assert "satisfies `evidence.pm_approval` only for the declared repository" in route
    assert "No additional GitHub comment is universally required" in route

    for clause in (
        "Writing blocks",
        "blockquotes",
        "indented lists",
        "heredocs",
        "--body-file",
        "set -e",
        "set -u",
        "set -o pipefail",
        "gh pr ready",
        "--merge --delete-branch",
        "--match-head-commit",
        "gh issue close",
        "git -C <local-path> branch -D <work-branch>",
        "Final read-only verification",
    ):
        assert clause in bundle
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


@pytest.mark.parametrize(
    (
        "kernel_path",
        "template_path",
        "operation_path",
        "contract_clauses",
        "template_clauses",
        "operation_clauses",
        "instruction_prefix",
        "instruction_clauses",
    ),
    (
        (
            "project-os-es/kernel/salidas.json",
            "project-os-es/templates/route-prompt.md",
            "project-os-es/operaciones/fase-3/MOS-3.4-draftear-route-prompt-de-implementacion.md",
            (
                "bootloader compacto e issue-referential",
                "issue o PR vivo como fuente del detalle de implementacion",
                "scope de 1-3 lineas que no restata",
                "un unico bloque estandar de variables seguido por una unica instruccion concreta",
            ),
            (
                "El bloque siguiente es el route prompt completo",
                "issue o PR vivo y sus comentarios",
                "No agregues encabezados, secciones, listas, checklists ni",
            ),
            (
                "**Comprobación de conformidad:**",
                "compara la salida con",
                "Comprímela si repite detalle",
                "`SCOPE` de 1-3",
                "falla cerrado con `output.status_result`",
                "**QA manual reproducible:**",
                "issue largo con comentarios extensos",
            ),
            "{{Una unica instruccion concreta:",
            (
                "re-resuelve el kernel",
                "lee la evidencia viva requerida",
                "verifica la entrega PM",
                "falla cerrado",
            ),
        ),
        (
            "project-os-en/kernel/outputs.json",
            "project-os-en/templates/route-prompt.md",
            "project-os-en/operations/phase-3/MOS-3.4-draft-implementation-route-prompt.md",
            (
                "compact, issue-referential bootloader",
                "live issue or PR as the source of implementation detail",
                "1-3 line scope that does not restate",
                "one standard variable block followed by one concrete instruction",
            ),
            (
                "The following block is the complete route prompt",
                "live issue or PR and its comments",
                "Do not add headings, sections, lists, checklists,",
            ),
            (
                "**Conformance check:**",
                "compare the output with",
                "Compress it when it repeats",
                "a 1-3 line `SCOPE`",
                "fail closed with\n`output.status_result`",
                "**Reproducible manual QA:**",
                "Use a long issue with extensive comments",
            ),
            "{{One concrete instruction:",
            (
                "re-resolve the kernel",
                "read the required live evidence",
                "verify PM delivery",
                "fail closed",
            ),
        ),
    ),
)
def test_route_prompt_contract_template_and_mos_3_4_keep_compact_issue_referential_shape(
    kernel_path: str,
    template_path: str,
    operation_path: str,
    contract_clauses: tuple[str, ...],
    template_clauses: tuple[str, ...],
    operation_clauses: tuple[str, ...],
    instruction_prefix: str,
    instruction_clauses: tuple[str, ...],
) -> None:
    """Guard durable shape; generated chat output still requires manual QA."""
    outputs = json.loads((REPO_ROOT / kernel_path).read_text(encoding="utf-8"))["outputs"]
    route_prompt = next(output for output in outputs if output["key"] == "output.route_prompt")
    contract = " ".join((route_prompt["use_for"], *route_prompt["must_include"]))
    for clause in contract_clauses:
        assert clause in contract

    template = (REPO_ROOT / template_path).read_text(encoding="utf-8")
    for clause in template_clauses:
        assert clause in template
    assert template.count("```text") == 1
    prompt_block = re.search(r"```text\n(?P<body>.*?)\n```", template, re.DOTALL)
    assert prompt_block
    prompt_lines = [line for line in prompt_block.group("body").splitlines() if line]
    assert sum(line.startswith("SCOPE =") for line in prompt_lines) == 1
    assert prompt_lines[-1].startswith(instruction_prefix)
    for clause in instruction_clauses:
        assert clause in prompt_lines[-1]
    assert sum(line.startswith("{{") for line in prompt_lines) == 1
    assert all(
        " = " in line or line.startswith("recommended_effort:")
        for line in prompt_lines[:-1]
    )

    operation = (REPO_ROOT / operation_path).read_text(encoding="utf-8")
    for clause in operation_clauses:
        assert clause in operation


@pytest.mark.parametrize(
    ("template_path", "operation_path", "template_clauses", "operation_clauses"),
    (
        (
            "project-os-es/templates/route-prompt.md",
            "project-os-es/operaciones/fase-3/MOS-3.4-draftear-route-prompt-de-implementacion.md",
            (
                "no entregado por el PM",
                "PM_AUTHORIZATION_STATUS=pending",
                "satisface `evidence.pm_approval` únicamente para el repositorio, workflow,\nmodo, rama y scope declarados",
                "No se exige un comentario adicional de GitHub como\ncondición universal",
                "ausente, desconocido o\ninferido falla cerrado",
            ),
            (
                "no entregado por el PM",
                "PM_AUTHORIZATION_STATUS` en `pending`",
                "satisface `evidence.pm_approval` únicamente para el repositorio, workflow,\nmodo, rama y scope declarados",
                "No se exige un comentario adicional de GitHub como\ncondición universal",
                "ausente, desconocido o\ninferido falla cerrado",
            ),
        ),
        (
            "project-os-en/templates/route-prompt.md",
            "project-os-en/operations/phase-3/MOS-3.4-draft-implementation-route-prompt.md",
            (
                "was not delivered by the PM",
                "PM_AUTHORIZATION_STATUS=pending",
                "satisfies `evidence.pm_approval` only for the declared repository, workflow,\nmode, branch, and scope",
                "No additional GitHub comment is universally required",
                "absent, unknown, or inferred status fails closed",
            ),
            (
                "was not\ndelivered by the PM",
                "PM_AUTHORIZATION_STATUS` set to `pending`",
                "satisfies `evidence.pm_approval` only for the declared repository, workflow,\nmode, branch, and scope",
                "No additional GitHub comment is universally required",
                "absent, unknown, or inferred status fails closed",
            ),
        ),
    ),
)
def test_route_prompt_authorization_requires_exact_pm_delivered_grant(
    template_path: str,
    operation_path: str,
    template_clauses: tuple[str, ...],
    operation_clauses: tuple[str, ...],
) -> None:
    for path, clauses in (
        (template_path, template_clauses),
        (operation_path, operation_clauses),
    ):
        text = (REPO_ROOT / path).read_text(encoding="utf-8")
        for clause in clauses:
            assert clause in text


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
