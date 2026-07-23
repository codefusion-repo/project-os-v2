"""Focused guards for the browser-first adoption normalization (issue #456).

Cover the kernel output/artifact contracts, the MOS-0.2..MOS-0.5 operation
prompts in both languages, the two-stage target-adoption resolution, the
adapter auditor readiness split, and the operation/kernel coherence validators.
"""

from __future__ import annotations

import json
import re
from io import StringIO
from pathlib import Path
from types import SimpleNamespace

import pytest

from dogfooding.tests.test_audit_target_adapters import (
    filled_browser_adapter,
    filled_spanish_adapter,
    write_terminal_adapters,
)
from dogfooding.tools.audit_target_adapters import (
    Source,
    evaluate_adoption_readiness,
    main as audit_main,
)
from tools.operation_prompt_wizard import (
    InputVariable,
    PM_AUTHORIZATION_GRANTED,
    PM_AUTHORIZATION_PENDING,
    PM_AUTHORIZATION_STATUS_NAME,
    discover_operations,
    operation_output_refs,
    operation_requires_route_prompt_path_selection,
    run_wizard,
    validate_variable_value,
)
from tools.project_os_resolve import resolve
from tools.validate_kernel import Finding, _check_operation_kernel_coherence


REPO_ROOT = Path(__file__).resolve().parents[2]
ES_KERNEL = REPO_ROOT / "project-os-es/kernel"
EN_KERNEL = REPO_ROOT / "project-os-en/kernel"

ADOPTION_CODES = ("MOS-0.2", "MOS-0.3", "MOS-0.4", "MOS-0.5")

KERNEL_FILES = {
    "es": {
        "workflows": (ES_KERNEL / "workflows.json", "workflows"),
        "outputs": (ES_KERNEL / "salidas.json", "outputs"),
        "artifacts": (ES_KERNEL / "artefactos.json", "artefactos"),
    },
    "en": {
        "workflows": (EN_KERNEL / "workflows.json", "workflows"),
        "outputs": (EN_KERNEL / "outputs.json", "outputs"),
        "artifacts": (EN_KERNEL / "artifacts.json", "artifacts"),
    },
}


def _load(family: tuple[Path, str]) -> list[dict]:
    path, collection = family
    return json.loads(path.read_text(encoding="utf-8"))[collection]


def answers(*values: str):
    iterator = iter(values)
    return lambda _prompt: next(iterator)


# --- Kernel contract guards -------------------------------------------------


@pytest.mark.parametrize("language", ("es", "en"))
def test_target_adoption_allows_draft_and_delegated_outputs(language: str) -> None:
    workflows = _load(KERNEL_FILES[language]["workflows"])
    target_adoption = next(w for w in workflows if w["key"] == "workflow.target_adoption")

    assert set(target_adoption["allowed_outputs"]) == {
        "output.adoption_packet",
        "output.route_prompt",
        "output.pm_command_bundle",
        "output.execution_report",
        "output.status_result",
    }


@pytest.mark.parametrize("language", ("es", "en"))
def test_adoption_packet_is_draft_only_and_execution_report_stays_mutable(language: str) -> None:
    outputs = {o["key"]: o for o in _load(KERNEL_FILES[language]["outputs"])}

    assert outputs["output.adoption_packet"]["action_class"] == "action.draft_only"
    assert outputs["output.adoption_packet"]["allows_non_material_gaps"] is False
    assert outputs["output.adoption_packet"]["safe_degradation_key"] is None
    assert outputs["output.execution_report"]["action_class"] == "action.mutable"
    assert "workflow.target_adoption" in outputs["output.execution_report"]["workflow_key"]


@pytest.mark.parametrize("language", ("es", "en"))
def test_route_prompt_and_pm_bundle_outputs_and_artifacts_include_target_adoption(
    language: str,
) -> None:
    outputs = {o["key"]: o for o in _load(KERNEL_FILES[language]["outputs"])}
    artifacts = {a["key"]: a for a in _load(KERNEL_FILES[language]["artifacts"])}

    for output_key in ("output.route_prompt", "output.pm_command_bundle"):
        assert "workflow.target_adoption" in outputs[output_key]["workflow_key"]
    assert "workflow.target_adoption" in artifacts["artefacto.route_prompt"]["workflow_key"]
    assert "workflow.target_adoption" in artifacts["artefacto.pm_command_bundle"]["workflow_key"]


@pytest.mark.parametrize(
    ("outputs_family", "template_path", "issue_clause", "scope_clause"),
    (
        (
            KERNEL_FILES["es"]["outputs"],
            REPO_ROOT / "project-os-es/templates/route-prompt.md",
            "issue o PR vivo como fuente del detalle de implementacion",
            "referencia viva de scope equivalente",
        ),
        (
            KERNEL_FILES["en"]["outputs"],
            REPO_ROOT / "project-os-en/templates/route-prompt.md",
            "live issue or PR as the source of implementation detail",
            "equivalent live scope reference",
        ),
    ),
)
def test_route_prompt_accepts_a_non_issue_live_scope_without_losing_issue_shape(
    outputs_family: tuple[Path, str],
    template_path: Path,
    issue_clause: str,
    scope_clause: str,
) -> None:
    """`workflow.target_adoption` routes a target-scoped unit; issue workflows keep theirs."""

    outputs = {o["key"]: o for o in _load(outputs_family)}
    contract = " ".join(outputs["output.route_prompt"]["must_include"])
    template = template_path.read_text(encoding="utf-8")

    for text in (contract, template):
        assert issue_clause in text or "issue-referential" in text
        assert scope_clause in text
    assert "evidence.issue_scope" in contract
    assert "evidence.issue_scope" in template
    assert "workflow.target_adoption" in template


# --- Operation prompt guards ------------------------------------------------


@pytest.mark.parametrize(
    "operations_dir",
    (REPO_ROOT / "project-os-es/operaciones", REPO_ROOT / "project-os-en/operations"),
)
def test_adoption_operations_never_assign_a_delegated_mode_to_browser_chat(
    operations_dir: Path,
) -> None:
    operations = {op.mos_code: op for op in discover_operations(operations_dir)}
    for code in ADOPTION_CODES:
        text = operations[code].text
        kernel_line = next(line for line in text.splitlines() if line.startswith("- Kernel:"))
        surface_line = next(
            line
            for line in text.splitlines()
            if line.startswith("- Superficie:") or line.startswith("- Surface:")
        )
        assert "mode.review_only" in kernel_line
        assert "mode.delegated_commit_pr" not in kernel_line
        assert surface_line.split(":", 1)[1].strip().startswith("browser_chat")


@pytest.mark.parametrize(
    "operations_dir",
    (REPO_ROOT / "project-os-es/operaciones", REPO_ROOT / "project-os-en/operations"),
)
def test_adoption_operations_require_no_adoption_issue_and_only_the_target(
    operations_dir: Path,
) -> None:
    """The bounded target adoption is the live unit; no adoption issue exists."""

    operations = {op.mos_code: op for op in discover_operations(operations_dir)}
    for code in ADOPTION_CODES:
        operation = operations[code]
        variables = {v.name: v for v in operation.variables}
        assert "ADOPTION_ISSUE_NUMBER" not in variables
        assert "ADOPTION_ISSUE_NUMBER" not in operation.text
        assert [name for name, v in variables.items() if v.required] == ["TARGET_REPOSITORY"]


@pytest.mark.parametrize(
    "operations_dir",
    (REPO_ROOT / "project-os-es/operaciones", REPO_ROOT / "project-os-en/operations"),
)
def test_adoption_operations_keep_the_roadmap_optional(operations_dir: Path) -> None:
    """A roadmap is optional live evidence, never an adoption prerequisite."""

    operations = {op.mos_code: op for op in discover_operations(operations_dir)}
    for code in ADOPTION_CODES:
        variables = {v.name: v for v in operations[code].variables}
        assert variables["ROADMAP_ISSUE"].required is False
        assert "{{#ROADMAP_ISSUE}}" not in operations[code].text


@pytest.mark.parametrize(
    "operations_dir",
    (REPO_ROOT / "project-os-es/operaciones", REPO_ROOT / "project-os-en/operations"),
)
def test_adoption_operations_declare_only_workflow_allowed_outputs(operations_dir: Path) -> None:
    language = "es" if operations_dir.name == "operaciones" else "en"
    workflows = _load(KERNEL_FILES[language]["workflows"])
    allowed = set(
        next(w for w in workflows if w["key"] == "workflow.target_adoption")["allowed_outputs"]
    )
    operations = {op.mos_code: op for op in discover_operations(operations_dir)}
    for code in ADOPTION_CODES:
        kernel_line = next(
            line for line in operations[code].text.splitlines() if line.startswith("- Kernel:")
        )
        for output in re.findall(r"output\.[a-z_]+", kernel_line):
            assert output in allowed, f"{code} declares {output} not allowed by target_adoption"


def test_mos_0_2_drafts_browser_first_and_never_invents_roadmap_bilingually() -> None:
    es = {op.mos_code: op for op in discover_operations(REPO_ROOT / "project-os-es/operaciones")}
    en = {op.mos_code: op for op in discover_operations(REPO_ROOT / "project-os-en/operations")}

    assert "roadmap_state=missing" in es["MOS-0.2"].text
    assert "no inventes su número" in es["MOS-0.2"].text
    assert "output.pm_command_bundle" in es["MOS-0.2"].text
    assert "roadmap_state=missing" in en["MOS-0.2"].text
    assert "do not invent its number" in en["MOS-0.2"].text
    assert "output.pm_command_bundle" in en["MOS-0.2"].text


def test_mos_0_5_separates_browser_and_terminal_readiness_bilingually() -> None:
    es = {op.mos_code: op for op in discover_operations(REPO_ROOT / "project-os-es/operaciones")}
    en = {op.mos_code: op for op in discover_operations(REPO_ROOT / "project-os-en/operations")}

    assert "browser_adoption_state" in es["MOS-0.5"].text
    assert "terminal_adoption_state" in es["MOS-0.5"].text
    assert "no suministrado" in es["MOS-0.5"].text
    assert "status.needs_context" in es["MOS-0.5"].text
    assert "browser_adoption_state" in en["MOS-0.5"].text
    assert "terminal_adoption_state" in en["MOS-0.5"].text
    assert "not supplied" in en["MOS-0.5"].text
    assert "status.needs_context" in en["MOS-0.5"].text


# --- Two-stage resolution ---------------------------------------------------


@pytest.mark.parametrize("kernel_dir", (ES_KERNEL, EN_KERNEL))
def test_target_adoption_resolves_browser_draft_and_terminal_write_stages(kernel_dir: Path) -> None:
    draft = resolve("actor.browser_chat", "workflow.target_adoption", "mode.review_only", kernel_dir=kernel_dir)
    assert draft["estado"] == "status.resolved"
    draft_outputs = {o["key"] for o in draft["resuelto"]["workflow"]["allowed_outputs"]}
    assert {"output.route_prompt", "output.pm_command_bundle", "output.adoption_packet"} <= draft_outputs
    draft_artifacts = {a["key"] for a in draft["resuelto"]["workflow"]["artefactos"]}
    assert {"artefacto.route_prompt", "artefacto.pm_command_bundle", "artefacto.paquete_adopcion"} <= draft_artifacts

    write = resolve(
        "actor.terminal_agent",
        "workflow.target_adoption",
        "mode.delegated_commit_pr",
        kernel_dir=kernel_dir,
    )
    assert write["estado"] == "status.resolved"
    write_outputs = {o["key"] for o in write["resuelto"]["workflow"]["allowed_outputs"]}
    assert "output.execution_report" in write_outputs


def test_browser_chat_cannot_resolve_a_delegated_adoption_mode() -> None:
    blocked = resolve("actor.browser_chat", "workflow.target_adoption", "mode.delegated_commit_pr")
    assert blocked["estado"] == "status.blocked"
    assert blocked["resuelto"] is None


# --- Adapter auditor readiness ---------------------------------------------


def test_readiness_is_needs_context_when_browser_content_is_not_supplied(tmp_path: Path) -> None:
    write_terminal_adapters(
        tmp_path,
        filled_spanish_adapter(
            tmp_path,
            target_path=str(tmp_path),
            kernel_path=str(REPO_ROOT / "project-os-es/kernel"),
        ),
    )

    findings, readiness = evaluate_adoption_readiness(tmp_path, expected_repository="example/target")

    assert readiness.browser == "not_supplied"
    assert readiness.terminal == "ready"
    assert readiness.overall == "needs_context"


def test_readiness_is_go_only_when_browser_and_terminal_are_ready(tmp_path: Path) -> None:
    write_terminal_adapters(
        tmp_path,
        filled_spanish_adapter(
            tmp_path,
            target_path=str(tmp_path),
            kernel_path=str(REPO_ROOT / "project-os-es/kernel"),
        ),
    )

    findings, readiness = evaluate_adoption_readiness(
        tmp_path,
        expected_repository="example/target",
        browser_chat=Source("BROWSER_CHAT.md", filled_browser_adapter(tmp_path)),
    )

    assert findings == []
    assert readiness.browser == "ready"
    assert readiness.terminal == "ready"
    assert readiness.overall == "go"


def test_readiness_is_no_go_when_terminal_adapter_is_missing(tmp_path: Path) -> None:
    findings, readiness = evaluate_adoption_readiness(
        tmp_path,
        expected_repository="example/target",
        browser_chat=Source("BROWSER_CHAT.md", filled_browser_adapter(tmp_path)),
    )

    assert readiness.browser == "ready"
    assert readiness.terminal == "missing"
    assert readiness.overall == "no_go"


def test_terminal_adapter_without_a_roadmap_anchor_is_ready(tmp_path: Path) -> None:
    """A target may adopt before it has any roadmap; the anchor is optional."""

    agents = filled_spanish_adapter(
        tmp_path,
        target_path=str(tmp_path),
        kernel_path=str(REPO_ROOT / "project-os-es/kernel"),
    )
    assert "roadmap canónico" in agents
    assert not re.search(r"#\d+", agents)
    write_terminal_adapters(tmp_path, agents)

    findings, readiness = evaluate_adoption_readiness(
        tmp_path,
        expected_repository="example/target",
        browser_chat=Source("BROWSER_CHAT.md", filled_browser_adapter(tmp_path)),
    )

    assert [f.code for f in findings if f.code.startswith("TAA-ROADMAP")] == []
    assert readiness.terminal == "ready"
    assert readiness.overall == "go"


def test_canonical_terminal_adapters_carry_no_durable_roadmap_placeholder() -> None:
    for path in (
        REPO_ROOT / "project-os-es/adapters/AGENTS.target.md",
        REPO_ROOT / "project-os-en/adapters/AGENTS.target.md",
        REPO_ROOT / "AGENTS.md",
    ):
        text = path.read_text(encoding="utf-8")
        assert "{{#ROADMAP_ISSUE}}" not in text, path
        assert not re.search(r"roadmap[^.\n]*`#\d+`", text), path


# --- Readiness CLI exit status ---------------------------------------------


def _readiness_exit(argv: list[str], capsys: pytest.CaptureFixture[str]) -> tuple[int, str]:
    code = audit_main(argv)
    return code, capsys.readouterr().out


def test_readiness_cli_exits_zero_only_for_go(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    write_terminal_adapters(
        tmp_path,
        filled_spanish_adapter(
            tmp_path,
            target_path=str(tmp_path),
            kernel_path=str(REPO_ROOT / "project-os-es/kernel"),
        ),
    )
    browser = tmp_path / "browser.md"
    browser.write_text(filled_browser_adapter(tmp_path), encoding="utf-8")

    code, out = _readiness_exit(
        [
            "--target",
            str(tmp_path),
            "--repository",
            "example/target",
            "--browser-chat",
            str(browser),
            "--readiness",
        ],
        capsys,
    )

    assert "overall=go" in out
    assert code == 0


def test_readiness_cli_fails_closed_on_needs_context_without_findings(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Zero findings plus an unaudited browser surface must not exit 0."""

    write_terminal_adapters(
        tmp_path,
        filled_spanish_adapter(
            tmp_path,
            target_path=str(tmp_path),
            kernel_path=str(REPO_ROOT / "project-os-es/kernel"),
        ),
    )

    code, out = _readiness_exit(
        ["--target", str(tmp_path), "--repository", "example/target", "--readiness"],
        capsys,
    )

    assert "browser=not_supplied" in out
    assert "overall=needs_context" in out
    assert "(0 finding(s))" in out
    assert code != 0


def test_readiness_cli_fails_closed_on_no_go(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    browser = tmp_path / "browser.md"
    browser.write_text(filled_browser_adapter(tmp_path), encoding="utf-8")

    code, out = _readiness_exit(
        [
            "--target",
            str(tmp_path),
            "--repository",
            "example/target",
            "--browser-chat",
            str(browser),
            "--readiness",
        ],
        capsys,
    )

    assert "overall=no_go" in out
    assert code != 0


def test_readiness_cli_reports_a_tooling_error_as_two(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    code = audit_main(
        [
            "--target",
            str(tmp_path / "missing"),
            "--repository",
            "example/target",
            "--readiness",
        ]
    )

    assert code == 2


def test_readiness_never_requires_browser_chat_as_a_repo_file(tmp_path: Path) -> None:
    write_terminal_adapters(
        tmp_path,
        filled_spanish_adapter(
            tmp_path,
            target_path=str(tmp_path),
            kernel_path=str(REPO_ROOT / "project-os-es/kernel"),
        ),
    )
    # No BROWSER_CHAT.md file exists in the checkout; supplying its content
    # externally is enough to reach a ready browser state.
    assert not (tmp_path / "BROWSER_CHAT.md").exists()

    _, readiness = evaluate_adoption_readiness(
        tmp_path,
        expected_repository="example/target",
        browser_chat=Source("BROWSER_CHAT.md", filled_browser_adapter(tmp_path)),
    )

    assert readiness.overall == "go"


# --- Operation/kernel coherence validators ---------------------------------


def _write_op(path: Path, code: str, surface: str, kernel: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"# {code} — Coherence probe\n\n"
        f"Operación MOSDLC `probe-{code.lower()}` · Fase 9 — Test · Riesgo: low.\n\n"
        f"- Superficie: {surface}\n"
        f"- Kernel: {kernel}\n"
        "- Evidencia: evidence.target_adoption\n"
        "- Aprobación PM: No\n",
        encoding="utf-8",
    )


def _surface(tmp_path: Path) -> SimpleNamespace:
    return SimpleNamespace(
        operations_dir=tmp_path,
        kernel_files={"artifacts": ("artefactos.json", "artefactos")},
    )


ACTORS = {
    "actor.browser_chat": {"key": "actor.browser_chat", "allowed_modes": ["mode.review_only"]},
    "actor.terminal_agent": {
        "key": "actor.terminal_agent",
        "allowed_modes": ["mode.review_only", "mode.delegated_commit_pr"],
    },
}
WORKFLOWS = {
    "workflow.target_adoption": {
        "key": "workflow.target_adoption",
        "allowed_outputs": ["output.adoption_packet", "output.route_prompt"],
    },
    "workflow.review_only": {
        "key": "workflow.review_only",
        "allowed_outputs": ["output.review_result"],
    },
}


def test_coherence_flags_a_browser_actor_with_a_delegated_mode(tmp_path: Path) -> None:
    _write_op(
        tmp_path / "MOS-9.1-probe.md",
        "MOS-9.1",
        "browser_chat → terminal_agent",
        "workflow.target_adoption · mode.delegated_commit_pr · output.adoption_packet",
    )
    findings: list[Finding] = []

    _check_operation_kernel_coherence(_surface(tmp_path), ACTORS, WORKFLOWS, [], findings)

    assert [f.code for f in findings] == ["OPS-020"]


def test_coherence_flags_an_output_not_allowed_by_the_workflow(tmp_path: Path) -> None:
    _write_op(
        tmp_path / "MOS-9.2-probe.md",
        "MOS-9.2",
        "browser_chat",
        "workflow.target_adoption · mode.review_only · output.execution_report",
    )
    findings: list[Finding] = []

    _check_operation_kernel_coherence(_surface(tmp_path), ACTORS, WORKFLOWS, [], findings)

    assert [f.code for f in findings] == ["OPS-021"]


def test_coherence_flags_an_artifact_output_the_workflow_disallows(tmp_path: Path) -> None:
    _write_op(
        tmp_path / "MOS-9.3-probe.md",
        "MOS-9.3",
        "browser_chat",
        "workflow.target_adoption · mode.review_only · output.adoption_packet",
    )
    artifacts = [
        {
            "key": "artefacto.bad",
            "output_key": "output.route_prompt",
            "workflow_key": ["workflow.review_only"],
        }
    ]
    findings: list[Finding] = []

    _check_operation_kernel_coherence(_surface(tmp_path), ACTORS, WORKFLOWS, artifacts, findings)

    assert [f.code for f in findings] == ["OPS-022"]


def test_coherence_accepts_a_browser_first_adoption_operation(tmp_path: Path) -> None:
    _write_op(
        tmp_path / "MOS-9.4-probe.md",
        "MOS-9.4",
        "browser_chat → terminal_agent",
        "workflow.target_adoption · mode.review_only · output.adoption_packet (+output.route_prompt)",
    )
    artifacts = [
        {
            "key": "artefacto.route_prompt",
            "output_key": "output.route_prompt",
            "workflow_key": ["workflow.target_adoption"],
        }
    ]
    findings: list[Finding] = []

    _check_operation_kernel_coherence(_surface(tmp_path), ACTORS, WORKFLOWS, artifacts, findings)

    assert findings == []


# --- Wizard route selection and variable validation -------------------------


def test_roadmap_issue_stays_optional_under_generic_numeric_validation() -> None:
    variable = InputVariable("ROADMAP_ISSUE", "<ROADMAP_ISSUE>", False, "")

    # Optional: a blank value is accepted, so a target with no roadmap can still
    # complete an adoption prompt.
    assert validate_variable_value(variable, "") is None
    assert validate_variable_value(variable, "not-a-number") is not None
    assert validate_variable_value(variable, "274") is None
    assert validate_variable_value(variable, "#274") is None


def test_mos_0_3_requires_explicit_route_path_selection() -> None:
    operation = next(op for op in discover_operations() if op.mos_code == "MOS-0.3")

    refs = operation_output_refs(operation)
    assert "output.route_prompt" in refs
    assert operation_requires_route_prompt_path_selection(operation) is True


ADOPTION_VALUES = ("codefusion-repo/project-os-v2", "", "", "", "", "")
"""TARGET_REPOSITORY plus the five optional adoption variables left blank."""


@pytest.mark.parametrize("language", ("es", "en"))
def test_mos_0_3_route_path_needs_no_adoption_issue_or_roadmap(
    language: str, tmp_path: Path
) -> None:
    """A route-capable adoption prompt completes with target scope alone."""

    output = run_wizard(
        language=language,
        output_dir=tmp_path,
        input_func=answers("MOS-0.3", *ADOPTION_VALUES, "1", "2", "write", "exit"),
        output_stream=StringIO(),
    )

    assert output is not None
    content = output.read_text(encoding="utf-8")
    assert "ADOPTION_ISSUE_NUMBER" not in content
    assert "ROADMAP_ISSUE=\n" in content
    assert "TARGET_REPOSITORY=codefusion-repo/project-os-v2" in content
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_GRANTED}" in content


@pytest.mark.parametrize("language", ("es", "en"))
def test_mos_0_3_route_path_keeps_pending_authorization_non_authorizing(
    language: str, tmp_path: Path
) -> None:
    output = run_wizard(
        language=language,
        output_dir=tmp_path,
        input_func=answers("MOS-0.3", *ADOPTION_VALUES, "1", "1", "write", "exit"),
        output_stream=StringIO(),
    )

    assert output is not None
    content = output.read_text(encoding="utf-8")
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_PENDING}" in content
    # The prose still explains what a granted status would mean; the rendered
    # INPUT line must stay pending and authorize nothing.
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_GRANTED}" not in content


@pytest.mark.parametrize("language", ("es", "en"))
def test_mos_0_3_non_route_path_omits_authorization(language: str, tmp_path: Path) -> None:
    output = run_wizard(
        language=language,
        output_dir=tmp_path,
        input_func=answers("MOS-0.3", *ADOPTION_VALUES, "2", "write", "exit"),
        output_stream=StringIO(),
    )

    assert output is not None
    content = output.read_text(encoding="utf-8")
    # The operation prose names PM_AUTHORIZATION_STATUS in its authorization
    # contract; the non-route path must not add it as a filled INPUT line.
    assert f"{PM_AUTHORIZATION_STATUS_NAME}=" not in content
